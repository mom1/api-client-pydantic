from datetime import date, datetime
from enum import Enum
from typing import List, Optional

import pytest
from apiclient import APIClient
from pydantic import BaseModel, Field

from apiclient_pydantic import serialize, serialize_all_methods


class Address(BaseModel):
    house_number: str = Field(alias='houseNumber')
    post_code: str = Field(alias='postCode')
    street: Optional[str]

    class Config:
        allow_population_by_field_name = True


class AccountHolder(BaseModel):
    first_name: str = Field(alias='firstName')
    last_name: str = Field(alias='lastName')
    middle_names: Optional[List[str]] = Field(alias='middleNames')
    address: Address
    date_of_birth: date = Field(alias='dob')

    class Config:
        allow_population_by_field_name = True


class AccountType(Enum):
    SAVING = 'SAVING'
    CURRENT = 'CURRENT'
    ISA = 'ISA'


class Account(BaseModel):
    account_number: int = Field(alias='accountNumber')
    sort_code: int = Field(alias='sortCode')
    account_type: AccountType = Field(alias='accountType')
    account_holder: AccountHolder = Field(alias='accountHolder')
    date_opened: datetime = Field(alias='dateOpened')

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


@pytest.fixture()
def unserialized():
    return {
        'accountHolder': {
            'address': {
                'houseNumber': '12B',
                'postCode': 'SW11 1AP',
            },
            'dob': '1980-02-28',
            'firstName': 'John',
            'lastName': 'Smith',
        },
        'account_number': 12345678,
        'accountType': 'SAVING',
        'sortCode': 989898,
        'dateOpened': '2020-11-03T12:32:12',
    }


@pytest.fixture()
def serialized(unserialized):
    return Account(**unserialized)


def test_serialize_request(unserialized, serialized):
    @serialize()
    def decorated_func(endpoint: str, custom: str, data: Account):
        return data

    @serialize()
    def decorated_func_args(endpoint: str, custom: str, data: Account):
        return custom

    @serialize()
    def decorated_func_kwargs(endpoint: str, data: Account, custom: str = 'tests'):
        return custom

    @serialize(Account)
    def decorated_func_schema(endpoint: str, data):
        return data

    @serialize()
    def decorated_func_no_schema(endpoint: str, **kwargs):
        return kwargs  # data as is

    got = decorated_func('', 'test', **unserialized)
    assert got == serialized.dict(by_alias=True, exclude_none=True)

    text = decorated_func_args('', custom='test', **unserialized)
    assert text == 'test'

    text = decorated_func_kwargs('', custom='test', **unserialized)
    assert text == 'test'

    got = decorated_func_schema('', **unserialized)
    assert got == serialized.dict(by_alias=True, exclude_none=True)

    got = decorated_func_no_schema('', **unserialized)
    assert got == unserialized


def test_serialize_response(unserialized, serialized):
    @serialize()
    def decorated_func(endpoint: str) -> Account:
        return unserialized

    got = decorated_func('')
    assert got == serialized


def test_serialize_all_methods(unserialized, serialized):
    @serialize_all_methods()
    class MyApiClient(APIClient):
        def decorated_func(self, data: Account) -> Account:
            return data

        def decorated_func_holder(self, data: AccountHolder) -> AccountHolder:
            return data

    client = MyApiClient()
    got = client.decorated_func(**unserialized)
    assert got == serialized

    got = client.decorated_func_holder(**unserialized.get('accountHolder'))
    assert got == serialized.account_holder
