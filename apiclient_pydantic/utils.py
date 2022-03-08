from typing import Any

import pydantic


def is_pydantic_model(cls: Any) -> bool:
    try:
        return issubclass(cls, pydantic.BaseModel)
    except TypeError:
        return False
