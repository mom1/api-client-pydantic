from functools import wraps
from typing import Callable, Optional, Type, get_type_hints

from pydantic import BaseModel, parse_obj_as


def serialize_request(schema: Optional[Type[BaseModel]] = None, extra_kwargs: dict = None):
    extra_kw = extra_kwargs or {'by_alias': True, 'exclude_none': True}

    def decorator(func: Callable) -> Callable:
        nonlocal schema
        map_schemas = None
        if not schema:
            map_schemas = {
                arg_name: arg_type
                for arg_name, arg_type in get_type_hints(func).items() if arg_name != 'return'
            }

        @wraps(func)
        def wrap(*args, **kwargs):
            if schema:
                instance = data = parse_obj_as(schema, kwargs)
                if isinstance(instance, BaseModel):
                    data = instance.dict(**extra_kw)
                return func(*args, data)
            elif map_schemas:
                data, origin_kwargs = {}, {}
                for arg_name, arg_type in map_schemas.items():
                    if issubclass(arg_type, BaseModel):
                        data[arg_name] = parse_obj_as(arg_type, kwargs).dict(**extra_kw)
                    else:
                        val = kwargs.get(arg_name)
                        if val is not None:
                            origin_kwargs[arg_name] = val
                new_kwargs = {**origin_kwargs, **data} or kwargs
                return func(*args, **new_kwargs)
            return func(*args, **kwargs)

        return wrap

    return decorator


def serialize_response(schema: Optional[Type[BaseModel]] = None):
    def decorator(func: Callable) -> Callable:
        nonlocal schema
        if not schema:
            schema = get_type_hints(func).get('return')

        @wraps(func)
        def wrap(*args, **kwargs) -> BaseModel:
            response = func(*args, **kwargs)
            if isinstance(response, (list, dict, tuple, set)) and schema:
                return parse_obj_as(schema, response)
            return response

        return wrap

    return decorator


def serialize(
    schema_request: Optional[Type[BaseModel]] = None,
    schema_response: Optional[Type[BaseModel]] = None,
    **base_kwargs,
):
    def decorator(func: Callable) -> Callable:
        response = func
        response = serialize_request(schema_request, extra_kwargs=base_kwargs)(func)
        response = serialize_response(schema_response)(response)

        return response

    return decorator


def serialize_all_methods(decorator=serialize):
    def decorate(cls):
        for attr, value in cls.__dict__.items():
            if callable(value) and not attr.startswith('_'):
                setattr(cls, attr, decorator()(value))
        return cls

    return decorate
