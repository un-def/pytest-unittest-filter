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


@pytest.fixture
def items(testdir, ini):
    return testdir.getitems("""
        import unittest

        class TestUnitFoo(unittest.TestCase):

            def test(self):
                assert True

        class TestUnitBar(unittest.TestCase):

            def test(self):
                assert True

        class CheckUnitFoo(unittest.TestCase):

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


def param(*expected, **options):
    id_ = ';'.join('{}={}'.format(*e) for e in options.items())
    return pytest.param(expected, id=id_, marks=pytest.mark.options(**options))


@pytest.mark.parametrize('expected_unittests', [
    param('TestUnitFoo', 'TestUnitBar', 'CheckUnitFoo'),
    param('TestUnitFoo', 'TestUnitBar', 'CheckUnitFoo', classes=''),
    param('TestUnitBar', 'CheckUnitFoo', classes='TestUn?tBar Check*'),
    param('TestUnitFoo', 'TestUnitBar', classes='Test'),
    param('TestUnitFoo', 'TestUnitBar', classes='Test*'),
    param('TestUnitFoo', 'CheckUnitFoo', classes='*Foo'),
    param('TestUnitFoo', 'CheckUnitFoo', classes='*Unit[!B]*'),
    param(classes='*Baz*'),
])
def test(testdir, items, expected_unittests):
    collected = sorted(item.nodeid.split('::')[1] for item in items)
    assert 'TestPytestFoo' in collected
    assert 'test_plain' in collected
    collected.remove('TestPytestFoo')
    collected.remove('test_plain')
    assert collected == sorted(expected_unittests)
