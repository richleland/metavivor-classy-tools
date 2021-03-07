import csv

import pytest


@pytest.fixture
def data_all_fields():
    with open("tests/data-all-fields.csv") as csvfile:
        data = csv.DictReader(csvfile)
        data = list(data)
    return data


@pytest.fixture
def data_no_page_ids():
    with open("tests/data-no-page-ids.csv") as csvfile:
        data = csv.DictReader(csvfile)
        data = list(data)
    return data
