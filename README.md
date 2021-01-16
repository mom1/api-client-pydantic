![GitHub issues](https://img.shields.io/github/issues/mom1/api-client-pydantic.svg)
![GitHub stars](https://img.shields.io/github/stars/mom1/api-client-pydantic.svg)
![GitHub Release Date](https://img.shields.io/github/release-date/mom1/api-client-pydantic.svg)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/mom1/api-client-pydantic/latest.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/mom1/api-client-pydantic.svg)
[![GitHub license](https://img.shields.io/github/license/mom1/api-client-pydantic)](https://github.com/mom1/api-client-pydantic/blob/master/LICENSE)

[![PyPI](https://img.shields.io/pypi/v/api-client-pydantic.svg)](https://pypi.python.org/pypi/api-client-pydantic)
[![PyPI](https://img.shields.io/pypi/pyversions/api-client-pydantic.svg)]()
![PyPI - Downloads](https://img.shields.io/pypi/dm/api-client-pydantic.svg?label=pip%20installs&logo=python)

# Python API Client Pydantic Extension

## Installation

```bash
pip install api-client-pydantic
```

## Usage

The following decorators have been provided to validate request data and converting json straight to pydantic class.

```python
from apiclient_pydantic import serialize, serialize_all_methods, serialize_request, serialize_response

# serialize incoming kwargs
@serialize_request(schema: Optional[Type[BaseModel]] = None, extra_kwargs: dict = None)

# serialize response in pydantic class
@serialize_response(schema: Optional[Type[BaseModel]] = None)

# serialize request and response data
@serialize(schema_request: Optional[Type[BaseModel]] = None, schema_response: Optional[Type[BaseModel]] = None, **base_kwargs)

# wraps all local methods of a class with a specified decorator. default 'serialize'
@serialize_all_methods(decorator=serialize)
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
2. Add the `@serialize_response` decorator to the api client method to transform the response
directly into your defined schema.
   ```python
   @serialize_response(List[Account])
   def get_accounts():
       ...
   # or
   @serialize_response()
   def get_accounts() -> List[Account]:
       ...
   ```
3. Add the `@serialize_request` decorator to the api client method to translate the incoming kwargs
into the required dict for the endpoint:
   ```python
   @serialize_request(AccountHolder)
   def create_account(data: dict):
      ...
   # or
   @serialize_request()
   def create_account(data: AccountHolder):
    # data will be exactly a dict
      ...
   create_account(last_name='Smith', first_name='John')
   # data will be a dict {"last_name": "Smith", "first_name": "John"}
   ```
4. `@serialize` - It is a combination of the two decorators `@serialize_response` and`@serialize_request`.
5. For more convenient use, you can wrap all APIClient methods with `@serialize_all_methods`.
   ```python
   from apiclient import APIClient
   from apiclient_pydantic import serialize_all_methods
   from typing import List

    from .models import Account, AccountHolder


    @serialize_all_methods()
    class MyApiClient(APIClient):
        def decorated_func(self, data: Account) -> Account:
            ...

        def decorated_func_holder(self, data: AccountHolder) -> List[Account]:
            ...
    ```
