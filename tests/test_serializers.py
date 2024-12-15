from functools import partial
from typing import Dict, List, Union

import pytest
from apiclient import APIClient
from pydantic import AfterValidator, BaseModel, BeforeValidator, ConfigDict, Field, ValidationError
from typing_extensions import Annotated

from apiclient_pydantic import ModelDumped, TModel, serialize, serialize_all_methods

ModelDumpedNotAlias = Annotated[TModel, AfterValidator(lambda v: v.model_dump(exclude_none=True, by_alias=False))]


class SimpleModel(BaseModel):
    test_attr: str = 'Param'


class SimpleConfigModel(BaseModel):
    test_attr: str = Field(alias='TestAttr')
    model_config = ConfigDict(populate_by_name=True)


class SimpleTestModel(BaseModel):
    test: str


class ForwardrefModel(BaseModel):
    test_attr: Annotated[str, BeforeValidator(str)] = 'Param'
    this: 'ForwardrefModel' = None


class ForbidModel(BaseModel):
    test_attr: str = 'Param'
    model_config = ConfigDict(extra='forbid')


@serialize_all_methods
class Client(APIClient):
    def function_without_all(self):
        return ['test']

    def function_simple_arg(self, pk: int):
        return pk

    def function_simple_response(self) -> int:
        return '1'

    def function_simple_response_and_arg(self, pk: int) -> bool:
        assert isinstance(pk, int)
        return pk

    def function_simple_auto_type_str(self, pk):
        return pk

    #
    def function_simple_args(self, *args):
        return args

    def function_simple_kwargs(self, **kwargs):
        return kwargs

    def function_simple_model(
        self,
        param: Annotated[ModelDumped[SimpleModel], Field(validate_default=True, default_factory=SimpleModel)] = None,
    ):
        return param

    def function_simple_model_args(self, param: ModelDumped[SimpleModel], test_attr: str):
        return test_attr, param

    def function_forbid_model(self, param: ModelDumped[ForbidModel]):
        return param

    @serialize(config=ConfigDict(arbitrary_types_allowed=True))
    def function_special_type(self, pk: None.__class__):
        return pk

    @serialize(validate_return=False)
    def function_return_none(self, pk=1) -> None:
        pass

    def function_forwardref(self, data: ModelDumped[ForwardrefModel]):
        return data

    def function_union(self, data: ModelDumped[Union[SimpleTestModel, SimpleModel]]):
        return data

    def function_list_response(self, data: ModelDumped[SimpleModel]) -> List[Dict[str, str]]:
        return [data]

    def function_config_test(self, data: ModelDumped[SimpleConfigModel]):
        return data

    def function_same_name_test(self, test_attr: ModelDumped[SimpleModel]):
        return test_attr

    async def async_function_simple_model(
        self,
        param: Annotated[ModelDumped[SimpleModel], Field(validate_default=True, default_factory=SimpleModel)] = None,
    ) -> SimpleTestModel:
        return {'test': param['test_attr']}

    async def async_function_return_none(self, param: SimpleModel) -> None:
        pass


@pytest.fixture()
def client() -> Client:
    return Client()


def test_function_without_all(client):
    assert client.function_without_all() == ['test']


def test_function_simple_arg(client):
    assert client.function_simple_arg(pk='1') == 1


def test_send_args(client):
    assert client.function_simple_arg('1') == 1


def test_function_simple_response(client):
    assert client.function_simple_response() == 1


def test_function_simple_response_and_arg(client):
    assert client.function_simple_response_and_arg(pk='0') is False


def test_function_simple_auto_type_str(client):
    assert client.function_simple_auto_type_str(pk='0') == '0'
    assert client.function_simple_auto_type_str(pk=0) == 0


def test_function_simple_args(client):
    assert client.function_simple_args('test') == ('test',)
    assert client.function_simple_args(111) == (111,)


def test_function_simple_kwargs(client):
    assert client.function_simple_kwargs(test='test') == {'test': 'test'}


def test_function_simple_model(client):
    assert client.function_simple_model() == {'test_attr': 'Param'}
    assert client.function_simple_model(param={'test_attr': 'test'}) == {'test_attr': 'test'}


def test_function_simple_model_args(client):
    assert client.function_simple_model_args(param={'test_attr': 'test'}, test_attr='test') == (
        'test',
        {'test_attr': 'test'},
    )


def test_function_forbid_model(client):
    assert client.function_forbid_model(param={'test_attr': 'test'}) == {'test_attr': 'test'}
    with pytest.raises(ValidationError):
        assert client.function_forbid_model(param={'test_attr': 'test', 'test': 'bla'})


def test_function_special_type(client):
    assert client.function_special_type(pk=None) is None
    with pytest.raises(ValidationError):
        assert client.function_special_type(pk=2)


def test_function_return_none(client):
    assert client.function_return_none(pk=2) is None


def test_function_forwardref(client):
    assert client.function_forwardref(data={'test_attr': '123', 'this': {'test_attr': 456}}) == {
        'test_attr': '123',
        'this': {'test_attr': '456'},
    }


def test_function_union(client):
    assert client.function_union(data={'test': 'bla'}) == {'test': 'bla'}
    assert client.function_union(data={'test_attr': 'bla'}) == {'test_attr': 'bla'}


def test_function_list_response(client):
    assert client.function_list_response(data={'test_attr': 'bla'}) == [{'test_attr': 'bla'}]


def test_function_config_test(client):
    assert client.function_config_test(data={'test_attr': 'bla'}) == {'TestAttr': 'bla'}


@pytest.mark.asyncio()
async def test_async_function_return_none(client):
    response = await client.async_function_return_none(param={'test_attr': 'test'})
    assert response is None


@pytest.mark.asyncio()
async def test_async_function_simple_model(client):
    response = await client.async_function_simple_model()
    assert isinstance(response, SimpleTestModel)
    assert response.model_dump(by_alias=True, exclude_none=True) == {'test': 'Param'}

    response = await client.async_function_simple_model(param={'test_attr': 'test'})
    assert isinstance(response, SimpleTestModel)
    assert response.model_dump(by_alias=True, exclude_none=True) == {'test': 'test'}


@pytest.mark.xfail()
def test_function_same_name_test(client):
    with pytest.raises(ValidationError):
        assert client.function_same_name_test(test_attr='bla') == {'test_attr': 'bla'}


def test_param_for_model():
    class MyModel(BaseModel):
        model_config = ConfigDict(populate_by_name=True)
        test: str = Field(alias='TesT')

    @serialize_all_methods()
    class Client1(APIClient):
        @serialize
        def function_by_alias(self, data: ModelDumped[MyModel]):
            return data

        @serialize
        def function(self, data: ModelDumpedNotAlias[MyModel]):
            return data

    client = Client1()
    assert client.function_by_alias(data={'TesT': 'bla'}) == {'TesT': 'bla'}
    assert client.function(data={'TesT': 'bla'}) == {'test': 'bla'}


def test_classmethod_error():
    with pytest.raises(TypeError, match='The `@classmethod` decorator should be applied after'):

        class Client2(APIClient):
            @serialize
            @classmethod
            def function(cls, data: ModelDumped[SimpleModel]):
                return data


def test_staticmethod_error():
    with pytest.raises(TypeError, match='The `@staticmethod` decorator should be applied after'):

        class Client2(APIClient):
            @serialize
            @staticmethod
            def function(_, data: ModelDumped[SimpleModel]):
                return data


def test_classmethod():
    class Client2(APIClient):
        @classmethod
        @serialize
        def function(cls, data: ModelDumped[SimpleModel]):
            return data

    client = Client2()
    assert client.function(data={'TesT': 'bla'}) == {'test_attr': 'Param'}


def test_partial_func():
    def function(data: ModelDumped[SimpleModel], test: str):
        return test, data

    func = partial(function, test='321')
    f = serialize(func)
    assert f({'test_attr': 'bla'}) == ('321', {'test_attr': 'bla'})


def test_response_model():
    class Client2(APIClient):
        @serialize(response=SimpleModel)
        def function_response_model(self):
            return {'test_attr': 'test1'}

    client = Client2()
    assert isinstance(client.function_response_model(), SimpleModel)
