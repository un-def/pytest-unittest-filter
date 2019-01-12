import pytest
from _pytest.unittest import UnitTestCase


__version__ = '0.2.1'


INI_OPTION_CLASSES = 'python_unittest_classes'
INI_OPTION_UNDERSCORE = 'python_unittest_exclude_underscore'


def pytest_addoption(parser):
    parser.addini(
        INI_OPTION_CLASSES,
        type='args',
        default=None,
        help='prefixes or glob names for unittest.TestCase subclass discovery',
    )
    parser.addini(
        INI_OPTION_UNDERSCORE,
        type='bool',
        default=False,
        help='prefixes or glob names for unittest.TestCase subclass discovery',
    )


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_pycollect_makeitem(collector, name):
    outcome = yield
    result = outcome.get_result()
    if result is None or not isinstance(result, UnitTestCase):
        return
    if collector.config.getini(INI_OPTION_UNDERSCORE) and name.startswith('_'):
        outcome.force_result(None)
        return
    if not collector.config.getini(INI_OPTION_CLASSES):
        return
    if not collector._matches_prefix_or_glob_option(INI_OPTION_CLASSES, name):
        outcome.force_result(None)
