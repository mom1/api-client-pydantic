from typing import List, Optional, Union

from apiclient import APIClient
from pydantic import BaseModel
from pydantic.config import Extra
from pydantic.fields import Field

from apiclient_pydantic import params_serializer, serialize_all_methods


class SimpleModel(BaseModel):
    test_attr: str = 'Param'


class SimpleConfigModel(BaseModel):
    test_attr: str = Field(alias='TestAttr')

    class Config:
        allow_population_by_field_name = True


class SimpleTestModel(BaseModel):
    test: str


class ForwardrefModel(BaseModel):
    test_attr: str = 'Param'
    this: Optional['ForwardrefModel'] = None


class ForbidModel(BaseModel):
    test_attr: str = 'Param'

    class Config:
        extra = Extra.forbid


@serialize_all_methods()
class Client(APIClient):
    def function_without_all(self):
        return ['test']

    def function_simple_arg(self, pk: int):
        return pk

    def function_simple_response(self) -> int:
        return '1'  # type: ignore

    def function_simple_response_and_arg(self, pk: int) -> bool:
        assert isinstance(pk, int)
        return pk  # type: ignore

    def function_simple_auto_type_str(self, pk):
        return pk

    def function_simple_args(self, *args):
        return args

    def function_simple_kwargs(self, **kwargs):
        return kwargs

    def function_simple_model(self, param: SimpleModel):
        return param

    def function_simple_model_args(self, param: SimpleModel, test_attr: str):
        return test_attr, param

    def function_forbid_model(self, param: ForbidModel):
        return param

    def function_type_from_default(self, pk=1):
        return pk

    def function_special_type(self, pk: None.__class__, name: ....__class__):  # type: ignore
        return pk, name

    def function_return_none(self, pk=1) -> None:
        pass

    def function_forwardref(self, data: 'ForwardrefModel'):
        return data

    def function_union(self, data: Union[SimpleTestModel, SimpleModel]):
        return data

    def function_list_response(self, data: SimpleModel) -> List[SimpleModel]:
        return [data]

    def function_config_test(self, data: SimpleConfigModel):
        return data


def test_function_without_all():
    client = Client()

    # not wrapped
    assert '__wrapped__' not in vars(client.function_without_all)

    assert client.function_without_all() == ['test']


def test_function_simple_arg():
    client = Client()

    # wrapped once
    assert '__wrapped__' in vars(client.function_simple_arg)
    assert '__wrapped__' not in vars(vars(client.function_simple_arg)['__wrapped__'])

    assert client.function_simple_arg(pk='1') == 1  # type: ignore


def test_send_args():
    client = Client()

    assert client.function_simple_arg('1') == 1  # type: ignore


def test_function_simple_response():
    client = Client()

    # wrapped once
    assert '__wrapped__' in vars(client.function_simple_response)
    assert '__wrapped__' not in vars(vars(client.function_simple_response)['__wrapped__'])

    assert client.function_simple_response() == 1  # type: ignore


def test_function_simple_response_and_arg():
    client = Client()

    # wrapped
    assert '__wrapped__' in vars(client.function_simple_response_and_arg)
    assert '__wrapped__' in vars(vars(client.function_simple_response_and_arg)['__wrapped__'])
    assert '__wrapped__' not in vars(vars(vars(client.function_simple_response_and_arg)['__wrapped__'])['__wrapped__'])

    assert client.function_simple_response_and_arg(pk='0') is False  # type: ignore


def test_function_simple_auto_type_str():
    client = Client()

    assert client.function_simple_auto_type_str(pk=0) == '0'


def test_function_simple_args():
    client = Client()

    assert client.function_simple_args('test') == ('test',)


def test_function_simple_kwargs():
    client = Client()

    assert client.function_simple_kwargs(test='test') == {'test': 'test'}


def test_function_simple_model():
    client = Client()

    assert client.function_simple_model() == {'test_attr': 'Param'}  # type: ignore
    assert client.function_simple_model(test_attr='test') == {'test_attr': 'test'}  # type: ignore


def test_function_simple_model_args():
    client = Client()

    assert client.function_simple_model_args(test_attr='test') == ('test', {'test_attr': 'test'})  # type: ignore


def test_function_forbid_model():
    client = Client()

    assert client.function_forbid_model(test_attr='test') == {'test_attr': 'test'}  # type: ignore
    assert client.function_forbid_model(test_attr='test', test='bla') == {'test_attr': 'test'}  # type: ignore


def test_function_type_from_default():
    client = Client()
    assert client.function_type_from_default(pk='2') == 2  # type: ignore


def test_function_special_type():
    client = Client()
    assert client.function_special_type(pk=2, name=True) == ('2', 'True')  # type: ignore


def test_function_return_none():
    client = Client()
    assert client.function_return_none(pk=2) is None  # type: ignore


def test_function_forwardref():
    client = Client()
    assert client.function_forwardref(test_attr='123', this={'test_attr': 456}) == {  # type: ignore
        'test_attr': '123',
        'this': {'test_attr': '456'},
    }


def test_function_union():
    client = Client()
    assert client.function_union(test='bla') == {'test': 'bla'}  # type: ignore
    assert client.function_union(test_attr='bla') == {'test_attr': 'bla'}  # type: ignore


def test_function_list_response():
    client = Client()
    assert client.function_list_response(test_attr='bla') == [{'test_attr': 'bla'}]  # type: ignore


def test_function_config_test():
    client = Client()
    assert client.function_config_test(test_attr='bla') == {'TestAttr': 'bla'}  # type: ignore


def test_param_for_model():
    class MyModel(BaseModel):
        test: str = Field(alias='TesT')

    @params_serializer()
    def function_by_alias(data: MyModel):
        return data

    @params_serializer(by_alias=False)
    def function(data: MyModel):
        return data

    assert function_by_alias(TesT='bla') == {'TesT': 'bla'}
    assert function(TesT='bla') == {'test': 'bla'}
