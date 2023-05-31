from datetime import datetime
from dataclasses import dataclass
import os
import pytest


@pytest.fixture
def execution_name():
    str_date = datetime.now().strftime("%Y%d%m%H%M%S")
    test_name = os.environ.get(
        'PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]

    name = f"{test_name}_{str_date}"

    return name
