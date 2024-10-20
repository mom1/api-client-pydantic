import inspect
from functools import partial
from typing import Any, Awaitable, Callable, Optional, Set, Type, TypeVar, Union

from apiclient import APIClient
from pydantic import AfterValidator, BaseModel, ConfigDict
from pydantic._internal import _generate_schema
from pydantic._internal._config import ConfigWrapper
from pydantic._internal._validate_call import ValidateCallWrapper as PydanticValidateCallWrapper
from pydantic.plugin._schema_validator import create_schema_validator
from typing_extensions import Annotated

try:  # pragma: no cover
    from pydantic._internal._typing_extra import get_module_ns_of as get_module
except ImportError:  # pragma: no cover
    from pydantic._internal._typing_extra import add_module_globals as get_module  # type: ignore[attr-defined,no-redef]


AnyCallableT = TypeVar('AnyCallableT', bound=Callable[..., Any])
T = TypeVar('T', bound=APIClient)

TModel = TypeVar('TModel', bound=BaseModel)
ModelDumped = Annotated[TModel, AfterValidator(lambda v: v.model_dump(exclude_none=True, by_alias=True))]


class ValidateCallWrapper(PydanticValidateCallWrapper):
    __slots__ = ('_response',)

    def __init__(
        self,
        function: Callable[..., Any],
        config: Optional[ConfigDict],
        validate_return: bool,
        response: Optional[Type[BaseModel]] = None,
    ) -> None:
        self.raw_function = function
        self._config = config
        self._validate_return = validate_return
        self._response = response
        self.__signature__ = inspect.signature(function)
        if isinstance(function, partial):
            func = function.func
            schema_type = func
            self.__name__ = f'partial({func.__name__})'
            self.__qualname__ = f'partial({func.__qualname__})'
            self.__annotations__ = func.__annotations__
            self.__module__ = func.__module__
            self.__doc__ = func.__doc__
        else:
            schema_type = function
            self.__name__ = function.__name__
            self.__qualname__ = function.__qualname__
            self.__annotations__ = function.__annotations__
            self.__module__ = function.__module__
            self.__doc__ = function.__doc__

        namespace = get_module(function)
        config_wrapper = ConfigWrapper(config)
        gen_schema = _generate_schema.GenerateSchema(config_wrapper, namespace)
        schema = gen_schema.clean_schema(gen_schema.generate_schema(function))
        self.__pydantic_core_schema__ = schema
        core_config = config_wrapper.core_config(self)

        self.__pydantic_validator__ = create_schema_validator(
            schema,
            schema_type,
            self.__module__,
            self.__qualname__,
            'validate_call',
            core_config,
            config_wrapper.plugin_settings,
        )
        if self._validate_return or self._response:
            return_type: Any
            if not (return_type := self._response):
                return_type = (
                    self.__signature__.return_annotation is not self.__signature__.empty
                    and self.__signature__.return_annotation
                    or Any
                )

            gen_schema = _generate_schema.GenerateSchema(config_wrapper, namespace)
            schema = gen_schema.clean_schema(gen_schema.generate_schema(return_type))
            self.__return_pydantic_core_schema__ = schema
            validator = create_schema_validator(
                schema,
                schema_type,
                self.__module__,
                self.__qualname__,
                'validate_call',
                core_config,
                config_wrapper.plugin_settings,
            )
            if inspect.iscoroutinefunction(self.raw_function):

                async def return_val_wrapper(aw: Awaitable[Any]) -> None:
                    return validator.validate_python(await aw)

                self.__return_pydantic_validator__ = return_val_wrapper
            else:
                self.__return_pydantic_validator__ = validator.validate_python
        else:
            self.__return_pydantic_core_schema__ = None
            self.__return_pydantic_validator__ = None  # type: ignore[assignment]
        self._name: Optional[str] = None  # set by __get__, used to set the instance attribute when decorating methods)

    def __get__(
        self,
        obj: Any,  # noqa: ANN401
        objtype: Optional[Type[Any]] = None,
    ) -> 'ValidateCallWrapper':  # pragma: no cover
        """Bind the raw function and return another ValidateCallWrapper wrapping that."""
        # Copy-paste to pass _response to the class
        if obj is None:
            try:
                # Handle the case where a method is accessed as a class attribute
                return objtype.__getattribute__(objtype, self._name)  # type: ignore[call-arg, arg-type]
            except AttributeError:
                # This will happen the first time the attribute is accessed
                pass

        bound_function = self.raw_function.__get__(obj, objtype)
        result = self.__class__(bound_function, self._config, self._validate_return, self._response)

        # skip binding to instance when obj or objtype has __slots__ attribute
        if hasattr(obj, '__slots__') or hasattr(objtype, '__slots__'):
            return result

        if self._name is not None:
            if obj is not None:
                object.__setattr__(obj, self._name, result)
            else:
                object.__setattr__(objtype, self._name, result)
        return result


APICLIENT_METHODS: Set[str] = {i[0] for i in inspect.getmembers(APIClient, predicate=inspect.isfunction)}


def serialize(
    __func: Optional[AnyCallableT] = None,
    *,
    config: Optional[ConfigDict] = None,
    validate_return: bool = True,
    response: Optional[Type[BaseModel]] = None,
) -> Union[Callable[[AnyCallableT], ValidateCallWrapper], ValidateCallWrapper]:
    def validate(function: AnyCallableT) -> ValidateCallWrapper:
        if isinstance(function, (classmethod, staticmethod)):
            name = type(function).__name__
            msg = f'The `@{name}` decorator should be applied after `@serialize` (put `@{name}` on top)'
            raise TypeError(msg)
        return ValidateCallWrapper(function, config, validate_return, response)

    if __func:
        return validate(__func)
    return validate


def serialize_all_methods(
    __cls: Optional[Type[T]] = None, config: Optional[ConfigDict] = None
) -> Union[AnyCallableT, Callable[[AnyCallableT], AnyCallableT], Callable[[Type[T]], Type[T]]]:
    def decorate(cls: Type[T]) -> Type[T]:
        for attr, value in vars(cls).items():
            if not attr.startswith('_') and inspect.isfunction(value) and attr not in APICLIENT_METHODS:
                setattr(cls, attr, serialize(value, config=config))
        return cls

    if __cls:
        return decorate(__cls)
    return decorate
