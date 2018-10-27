import pytest
from _pytest.unittest import UnitTestCase


__version__ = '0.1.0'


INI_OPTION_NAME = 'python_unittest_classes'


def pytest_addoption(parser):
    parser.addini(
        INI_OPTION_NAME,
        type='args',
        default=None,
        help='prefixes or glob names for unittest.TestCase subclass discovery',
    )


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_pycollect_makeitem(collector, name):
    outcome = yield
    if not collector.config.getini(INI_OPTION_NAME):
        return
    result = outcome.get_result()
    if result is None or not isinstance(result, UnitTestCase):
        return
    if not collector._matches_prefix_or_glob_option(INI_OPTION_NAME, name):
        outcome.force_result(None)
