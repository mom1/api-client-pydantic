from typing import Any

from pydantic.v1 import BaseModel


def is_pydantic_model(cls: Any) -> bool:
    try:
        return issubclass(cls, BaseModel)
    except TypeError:
        return False
