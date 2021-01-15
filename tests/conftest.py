import os

import pytest
import vcr

BASE_DIR = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
VCR_CASSETTE_DIR = os.path.join(BASE_DIR, 'vcr_cassettes')

api_client_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir=VCR_CASSETTE_DIR,
    record_mode='once',
    match_on=['uri', 'method', 'query'],
)

error_cassette_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir=VCR_CASSETTE_DIR,
    record_mode='once',
    match_on=['uri'],
)


@pytest.fixture
def cassette():
    with api_client_vcr.use_cassette('cassette.yaml') as cassette:
        yield cassette


@pytest.fixture
def error_cassette():
    with error_cassette_vcr.use_cassette('error_cassette.yaml') as cassette:
        yield cassette
