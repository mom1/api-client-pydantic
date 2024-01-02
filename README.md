![GitHub issues](https://img.shields.io/github/issues/mom1/api-client-pydantic.svg)
![GitHub stars](https://img.shields.io/github/stars/mom1/api-client-pydantic.svg)
![GitHub Release Date](https://img.shields.io/github/release-date/mom1/api-client-pydantic.svg)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/mom1/api-client-pydantic/latest.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/mom1/api-client-pydantic.svg)
[![GitHub license](https://img.shields.io/github/license/mom1/api-client-pydantic)](https://github.com/mom1/api-client-pydantic/blob/master/LICENSE)

[![PyPI](https://img.shields.io/pypi/v/api-client-pydantic.svg)](https://pypi.python.org/pypi/api-client-pydantic)
[![PyPI](https://img.shields.io/pypi/pyversions/api-client-pydantic.svg)]()
![PyPI - Downloads](https://img.shields.io/pypi/dm/api-client-pydantic.svg?label=pip%20installs&logo=python)

<a href="https://gitmoji.dev"><img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg" alt="Gitmoji"></a>
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# Python API Client Pydantic Extension

## Installation

```bash
pip install api-client-pydantic
```

## Usage

The following decorators have been provided to validate request data and converting json straight to pydantic class.

```python
from apiclient_pydantic import serialize, serialize_all_methods


# serialize request and response data
@serialize(config: Optional[ConfigDict] = None, validate_return: bool = True, response: Optional[Type[BaseModel]] = None)

# wraps all local methods of a class with a decorator 'serialize'.
@serialize_all_methods(config: Optional[ConfigDict] = None)
```

Usage:

1. Define the schema for your api in pydantic classes.
    ```python
    from pydantic import BaseModel, Field


    class Account(BaseModel):
        account_number: int = Field(alias='accountNumber')
        sort_code: int = Field(alias='sortCode')
        date_opened: datetime = Field(alias='dateOpened')
    ```

2. Add the `@serialize` decorator to the api client method to transform the response
   directly into your defined schema.
   ```python
    @serialize(response=List[Account])
    def get_accounts():
        ...
    # or
    @serialize
    def get_accounts() -> List[Account]:
        ...
    ```
3. Add the `@serialize` decorator to the api client method to translate the incoming kwargs
   into the required dict or instance for the endpoint:
   ```python
    from apiclient_pydantic import ModelDumped

    @serialize
    def create_account(data: AccountHolder):
        # data will be AccountHolder instance
        ...

    create_account(data={'last_name' : 'Smith','first_name' : 'John'})
    # data will be a AccountHolder(last_name="Smith", first_name="John")

    @serialize
    def create_account(data: ModelDumped[AccountHolder]):
        # data will be exactly a dict
        ...

    create_account(data={'last_name' : 'Smith','first_name' : 'John'})
    # data will be a dict {"last_name": "Smith", "first_name": "John"}
    ```
4. For more convenient use, you can wrap all APIClient methods with `@serialize_all_methods`.
   ```python
    from apiclient import APIClient
    from apiclient_pydantic import serialize_all_methods
    from typing import List

    from .models import Account, AccountHolder


    @serialize_all_methods
    class MyApiClient(APIClient):
        def decorated_func(self, data: Account) -> Account:
            ...

        def decorated_func_holder(self, data: AccountHolder) -> List[Account]:
            ...
    ```

## Related projects

### apiclient-pydantic-generator - Now deprecated.

This code generator creates a [ApiClient](https://github.com/MikeWooster/api-client) app from an openapi file.

[apiclient-pydantic-generator](https://github.com/mom1/apiclient-pydantic-generator)
