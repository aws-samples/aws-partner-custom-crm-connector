"""
Provides Configuration test functions.
"""

import os
from datetime import datetime
import pytest

@pytest.fixture
def execution_name():
    """Returns the name of the test in the format {TESTNAME_DATE}"""
    str_date = datetime.now().strftime("%Y%d%m%H%M%S")
    test_name = os.environ.get(
        'PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
    name = f"{test_name}_{str_date}"
    return name
