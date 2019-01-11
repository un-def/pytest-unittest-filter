import pytest


@pytest.fixture
def ini(request, testdir):
    marker = request.node.get_closest_marker('options')
    if not marker or not marker.kwargs:
        return
    ini_lines = ['[pytest]']
    ini_lines.extend(
        'python_unittest_{} = {}'.format(*e) for e in marker.kwargs.items())
    return testdir.makeini(ini_lines)


def get_collected(items):
    return sorted(item.nodeid.split('::')[1] for item in items)


def param(*expected, **options):
    id_ = ';'.join('{}={}'.format(*e) for e in options.items())
    return pytest.param(expected, id=id_, marks=pytest.mark.options(**options))


@pytest.mark.parametrize('expected_unittests', [
    # without options
    param(
        '_TestUnitFoo', 'TestUnitFoo', 'TestUnitBar', 'CheckUnitFoo',
        '_CheckUnitBar',),
    # with python_unittest_classes
    param(
        '_TestUnitFoo', 'TestUnitFoo', 'TestUnitBar', 'CheckUnitFoo',
        '_CheckUnitBar', classes=''),
    param('TestUnitFoo', 'TestUnitBar', classes='Test'),
    param('TestUnitFoo', 'TestUnitBar', classes='Test*'),
    param('TestUnitBar', 'CheckUnitFoo', classes='TestUn?tBar Check*'),
    param('_TestUnitFoo', 'TestUnitFoo', 'CheckUnitFoo', classes='*Foo'),
    param('TestUnitFoo', 'CheckUnitFoo', classes='[!_]*Foo'),
    param('_TestUnitFoo', 'TestUnitFoo', 'CheckUnitFoo', classes='*Unit[!B]*'),
    param('TestUnitFoo', 'TestUnitBar', 'CheckUnitFoo', classes='[!_]*'),
    param(classes='*Baz*'),
    # with python_unittest_exclude_underscore
    param(
        '_TestUnitFoo', 'TestUnitFoo', 'TestUnitBar', 'CheckUnitFoo',
        '_CheckUnitBar', exclude_underscore=False),
    param(
        'TestUnitFoo', 'TestUnitBar', 'CheckUnitFoo', exclude_underscore=True),
    # with python_unittest_classes and python_unittest_exclude_underscore
    param(
        '_TestUnitFoo', 'TestUnitFoo', 'CheckUnitFoo',
        classes='*Foo', exclude_underscore=False),
    param(
        'TestUnitFoo', 'CheckUnitFoo',
        classes='*Foo', exclude_underscore=True),
    param(
        '_CheckUnitBar', classes='*Check*Bar', exclude_underscore=False),
    param(classes='*Check*Bar', exclude_underscore=True),
])
def test_options(testdir, ini, expected_unittests):
    items = testdir.getitems("""
        import unittest

        class _TestUnitFoo(unittest.TestCase):

            def test(self):
                assert True

        class TestUnitFoo(unittest.TestCase):

            def test(self):
                assert True

        class TestUnitBar(unittest.TestCase):

            def test(self):
                assert True

        class CheckUnitFoo(unittest.TestCase):

            def test(self):
                assert True

        class _CheckUnitBar(unittest.TestCase):

            def test(self):
                assert True

        class TestPytestFoo(object):

            def test(self):
                assert True

        class CheckPytestBar(object):

            def test(self):
                assert True

        def test_plain():
            assert True
    """)
    collected = get_collected(items)
    assert 'TestPytestFoo' in collected
    assert 'test_plain' in collected
    collected.remove('TestPytestFoo')
    collected.remove('test_plain')
    assert collected == sorted(expected_unittests)


@pytest.mark.options(exclude_underscore=True, classes='*Bar')
def test_only_unittests_are_filtered(testdir, ini):
    testdir.makeconftest("""
        from _pytest.python import Class

        def pytest_pycollect_makeitem(collector, name):
            if name.startswith('_XTestClass'):
                return Class(name, parent=collector)
    """)
    items = testdir.getitems("""
        class _XTestClassFoo(object):

            def test(self):
                assert True
    """)
    collected = get_collected(items)
    assert collected == ['_XTestClassFoo']
