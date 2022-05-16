import asyncio
import inspect
from functools import wraps
from typing import Any, Callable, Dict, ForwardRef, Optional, Set, Tuple, Type, get_type_hints

from pydantic import BaseModel, create_model, parse_obj_as
from pydantic.config import BaseConfig as PydanticBaseConfig, Extra
from pydantic.typing import evaluate_forwardref

from .utils import is_pydantic_model

DictStrAny = Dict[str, Any]


class BaseConfig(PydanticBaseConfig):
    orm_mode = True


class ParamsObject:
    def __init__(self, **kwargs: DictStrAny) -> None:
        for attr, param in kwargs.items():
            setattr(self, attr, param)


def get_typed_signature(call: Callable) -> inspect.Signature:
    """Finds call signature and resolves all forwardrefs"""
    signature = inspect.signature(call)
    globalns = getattr(call, '__globals__', {})
    typed_params = [
        inspect.Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=get_typed_annotation(param, globalns),
        )
        for param in signature.parameters.values()
    ]
    typed_signature = inspect.Signature(typed_params)
    return typed_signature


def get_typed_annotation(param: inspect.Parameter, globalns: DictStrAny) -> Any:
    annotation = param.annotation
    if isinstance(annotation, str):
        annotation = make_forwardref(annotation, globalns)
    return annotation


def make_forwardref(annotation: str, globalns: DictStrAny) -> Any:
    forward_ref = ForwardRef(annotation)
    return evaluate_forwardref(forward_ref, globalns, globalns)


class ParamsSerializer:
    __slot__ = (
        'signature',
        'by_alias',
        'exclude_unset',
        'exclude_defaults',
        'exclude_none',
        'has_kwargs',
        'model_param',
        'params_object_class',
        'used_args_index',
    )

    params_object_class = ParamsObject
    used_args_index: Set = set()

    def __init__(
        self,
        by_alias: bool = True,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
    ):
        self.by_alias = by_alias
        self.exclude_unset = exclude_unset
        self.exclude_defaults = exclude_defaults
        self.exclude_none = exclude_none
        self.has_self = False
        self.has_kwargs = False

    def __call__(self, func: Callable) -> Callable:
        attrs, self.signature = {}, get_typed_signature(func)
        new_signature_parameters: DictStrAny = {}
        forbid_attrs = set()

        for name, arg in self.signature.parameters.items():
            if name == 'self':
                new_signature_parameters.setdefault(arg.name, arg)
                self.has_self = True
                continue

            if arg.kind == arg.VAR_KEYWORD:
                # Skipping **kwargs
                self.has_kwargs = True
                continue

            if arg.kind == arg.VAR_POSITIONAL:
                # Skipping *args
                continue

            arg_type = self._get_param_type(arg)

            if name not in new_signature_parameters:
                if is_pydantic_model(arg_type):
                    new_signature_parameters.update(
                        {argument.name: argument for argument in inspect.signature(arg_type).parameters.values()}
                    )
                else:
                    new_signature_parameters.setdefault(arg.name, arg)

            attrs[name] = (arg_type, ...)
            if is_pydantic_model(arg_type) and getattr(arg_type.Config, 'extra', None) == Extra.forbid:
                forbid_attrs.add(name)
        if attrs:
            config_cls = type(f'{func.__name__}Config', (BaseConfig,), {'forbid_attrs': forbid_attrs})
            self.model_param = create_model(f'{func.__name__}Params', __config__=config_cls, **attrs)  # type: ignore

        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def wrap(*args, **kwargs):
                params_object = self.make_object_params(args, kwargs)
                result = self.make_result(params_object)

                return await func(
                    *tuple(v for i, v in enumerate(args) if i not in self.used_args_index),
                    **result,
                )

        else:

            @wraps(func)
            def wrap(*args, **kwargs):
                params_object = self.make_object_params(args, kwargs)
                result = self.make_result(params_object)

                return func(
                    *tuple(v for i, v in enumerate(args) if i not in self.used_args_index),
                    **result,
                )

        # Override signature
        if new_signature_parameters and attrs:
            sig = inspect.signature(func)
            sig = sig.replace(parameters=tuple(sorted(new_signature_parameters.values(), key=lambda x: x.kind)))
            wrap.__signature__ = sig  # type: ignore

        return wrap if attrs else func

    def make_object_params(self, args: Tuple, kwargs: DictStrAny) -> ParamsObject:
        object_params = {}
        used_args_index = self.used_args_index
        forbid_attrs = getattr(self.model_param.Config, 'forbid_attrs', {})
        len_args = len(args)

        for index, (name, fld) in enumerate(self.model_param.__fields__.items(), start=int(self.has_self)):
            kw = kwargs
            if name in kwargs:
                kw = kwargs[name]
            elif len_args > index:
                kw = args[index]
                used_args_index.add(index)

            object_params[name] = kw
            if is_pydantic_model(fld.type_) and name in forbid_attrs and isinstance(kw, dict):
                object_params[name] = {k: v for k, v in kw.items() if k in fld.type_.__fields__}

        return self.params_object_class(**object_params)

    def make_result(self, params_object: ParamsObject) -> DictStrAny:
        return self.model_param.from_orm(params_object).dict(
            by_alias=self.by_alias,
            exclude_unset=self.exclude_unset,
            exclude_defaults=self.exclude_defaults,
            exclude_none=self.exclude_none,
        )

    def _get_param_type(self, arg: inspect.Parameter) -> Any:
        annotation = arg.annotation

        if annotation == self.signature.empty:
            if arg.default == self.signature.empty:
                annotation = str
            else:
                annotation = type(arg.default)

        if annotation is type(None) or annotation is type(Ellipsis):  # noqa: E721
            annotation = str

        return annotation


serialize_request = params_serializer = ParamsSerializer


class ResponseSerializer:
    __slot__ = ('response',)

    def __init__(self, response: Optional[Type[BaseModel]] = None):
        self.response = response

    def __call__(self, func: Callable) -> Callable:
        self.response = self.response or get_type_hints(func).get('return')
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def wrap(*args, **kwargs):
                result = await func(*args, **kwargs)
                if result is not None:
                    return parse_obj_as(self.response, result)
                return result

        else:

            @wraps(func)
            def wrap(*args, **kwargs):
                result = func(*args, **kwargs)
                if result is not None:
                    return parse_obj_as(self.response, result)
                return result

        return wrap if self.response else func


serialize_response = response_serializer = ResponseSerializer


def serialize(
    response: Optional[Type[BaseModel]] = None,
    by_alias: bool = True,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = True,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        result_func = ParamsSerializer(
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )(func)
        result_func = serialize_response(response=response)(result_func)

        return result_func

    return decorator


def serialize_all_methods(decorator=serialize):
    def decorate(cls):
        for attr, value in vars(cls).items():
            if not attr.startswith('_') and (inspect.ismethod(value) or inspect.isfunction(value)):
                setattr(cls, attr, decorator()(value))
        return cls

    return decorate
