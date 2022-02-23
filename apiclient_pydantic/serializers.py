import inspect
from functools import wraps
from typing import Any, Callable, Dict, Optional, Tuple, Type, Union, get_type_hints

from pydantic import BaseModel, parse_obj_as


def serialize_request(schema: Optional[Type[BaseModel]] = None, extra_kwargs: Dict[str, Any] = None) -> Callable:
    extra_kw = extra_kwargs or {'by_alias': True, 'exclude_none': True}

    def decorator(func: Callable) -> Callable:
        nonlocal schema
        map_schemas = {}
        parameters = []

        if schema:
            parameters.extend(list(inspect.signature(schema).parameters.values()))
        else:
            for arg_name, arg_type in get_type_hints(func).items():
                if arg_name == 'return':
                    continue
                map_schemas[arg_name] = arg_type
                if inspect.isclass(arg_type) and issubclass(arg_type, BaseModel):
                    parameters.extend(list(inspect.signature(arg_type).parameters.values()))

        @wraps(func)
        def wrap(*args, **kwargs):
            if schema:
                instance = data = parse_obj_as(schema, kwargs)
                data = instance.dict(**extra_kw)
                return func(*args, data)
            elif map_schemas:
                data, origin_kwargs = {}, {}
                for arg_name, arg_type in map_schemas.items():
                    if inspect.isclass(arg_type) and issubclass(arg_type, BaseModel):
                        data[arg_name] = parse_obj_as(arg_type, kwargs).dict(**extra_kw)
                    else:
                        val = kwargs.get(arg_name)
                        if val is not None:
                            origin_kwargs[arg_name] = val
                new_kwargs = {**origin_kwargs, **data} or kwargs
                return func(*args, **new_kwargs)
            return func(*args, **kwargs)

        # Override signature
        if parameters:
            sig = inspect.signature(func)
            _self_param = sig.parameters.get('self')
            self_param = [_self_param] if _self_param else []
            sig = sig.replace(parameters=tuple(self_param + parameters))
            wrap.__signature__ = sig  # type: ignore
        return wrap

    return decorator


def serialize_response(schema: Optional[Type[BaseModel]] = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        nonlocal schema
        if not schema:  # pragma: no cover
            schema = get_type_hints(func).get('return')

        @wraps(func)
        def wrap(*args: Tuple[Any], **kwargs: Dict[str, Any]) -> Union[BaseModel, Any]:
            response = func(*args, **kwargs)
            if isinstance(response, (list, dict, tuple, set)) and schema:
                return parse_obj_as(schema, response)
            return response

        return wrap

    return decorator


def serialize(
    schema_request: Optional[Type[BaseModel]] = None,
    schema_response: Optional[Type[BaseModel]] = None,
    **base_kwargs: Dict[str, Any],
) -> Callable:
    def decorator(func: Callable) -> Callable:
        response = func
        response = serialize_request(schema_request, extra_kwargs=base_kwargs)(func)
        response = serialize_response(schema_response)(response)

        return response

    return decorator


def serialize_all_methods(decorator=serialize):
    def decorate(cls):
        for attr, value in vars(cls).items():
            if not attr.startswith('_') and (inspect.ismethod(value) or inspect.isfunction(value)):
                setattr(cls, attr, decorator()(value))
        return cls

    return decorate
