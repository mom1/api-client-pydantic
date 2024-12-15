from __future__ import annotations

import inspect
from functools import partial
from typing import TYPE_CHECKING, Annotated, Any, Callable, TypeVar, cast

from apiclient import APIClient
from pydantic import AfterValidator, BaseModel, ConfigDict
from pydantic._internal import _generate_schema, _typing_extra, _validate_call
from pydantic._internal._config import ConfigWrapper
from pydantic._internal._generate_schema import GenerateSchema, ValidateCallSupportedTypes
from pydantic._internal._namespace_utils import MappingNamespace, NsResolver, ns_for_function
from pydantic._internal._validate_call import (
    ValidateCallWrapper as PydanticValidateCallWrapper,
    extract_function_qualname,
)
from pydantic.plugin._schema_validator import create_schema_validator
from pydantic.validate_call_decorator import _check_function_type

if TYPE_CHECKING:
    from collections.abc import Awaitable

T = TypeVar('T', bound=APIClient)
AnyCallableT = TypeVar('AnyCallableT', bound=Callable[..., Any])
TModel = TypeVar('TModel', bound=BaseModel)
ModelDumped = Annotated[TModel, AfterValidator(lambda v: v.model_dump(exclude_none=True, by_alias=True))]


class ValidateCallWrapper(PydanticValidateCallWrapper):
    __slots__ = ()

    def __init__(
        self,
        function: ValidateCallSupportedTypes,
        config: ConfigDict | None,
        validate_return: bool,
        parent_namespace: MappingNamespace | None,
        response: type[BaseModel] | None = None,
    ) -> None:
        super().__init__(function, config, validate_return, parent_namespace)
        if response:
            if isinstance(function, partial):  # pragma: no cover
                schema_type = function.func
                module = function.func.__module__
            else:
                schema_type = function
                module = function.__module__
            qualname = extract_function_qualname(function)

            ns_resolver = NsResolver(namespaces_tuple=ns_for_function(schema_type, parent_namespace=parent_namespace))
            config_wrapper = ConfigWrapper(config)
            core_config = config_wrapper.core_config(title=qualname)

            gen_schema = GenerateSchema(config_wrapper, ns_resolver)
            schema = gen_schema.clean_schema(gen_schema.generate_schema(response))
            validator = create_schema_validator(
                schema,
                schema_type,
                module,
                qualname,
                'validate_call',
                core_config,
                config_wrapper.plugin_settings,
            )
            if inspect.iscoroutinefunction(function):  # pragma: no cover

                async def return_val_wrapper(aw: Awaitable[Any]) -> None:
                    return validator.validate_python(await aw)

                self.__return_pydantic_validator__ = return_val_wrapper
            else:
                self.__return_pydantic_validator__ = validator.validate_python


APICLIENT_METHODS: set[str] = {i[0] for i in inspect.getmembers(APIClient, predicate=inspect.isfunction)}


def serialize(
    __func: AnyCallableT | None = None,
    /,
    *,
    config: ConfigDict | None = None,
    validate_return: bool = True,
    response: type[BaseModel] | None = None,
) -> AnyCallableT | Callable[[AnyCallableT], AnyCallableT]:
    parent_namespace = _typing_extra.parent_frame_namespace()

    def validate(function: AnyCallableT) -> AnyCallableT:
        _check_function_type(function)
        validate_call_wrapper = ValidateCallWrapper(
            cast(_generate_schema.ValidateCallSupportedTypes, function),
            config,
            validate_return,
            parent_namespace,
            response,
        )
        return _validate_call.update_wrapper_attributes(function, validate_call_wrapper.__call__)  # type:ignore[arg-type]

    if __func:
        return validate(__func)
    return validate


def serialize_all_methods(
    __cls: type[T] | None = None, /, *, config: ConfigDict | None = None
) -> AnyCallableT | Callable[[AnyCallableT], AnyCallableT] | Callable[[type[T]], type[T]]:
    def decorate(cls: type[T]) -> type[T]:
        for attr, value in vars(cls).items():
            if not attr.startswith('_') and inspect.isfunction(value) and attr not in APICLIENT_METHODS:
                setattr(cls, attr, serialize(value, config=config))
        return cls

    if __cls:
        return decorate(__cls)
    return decorate
