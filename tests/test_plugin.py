import pytest


@pytest.mark.parametrize('option_value, expected_unittests', [
    (None, ('TestUnitFoo', 'TestUnitBar', 'CheckUnitFoo')),
    ('', ('TestUnitFoo', 'TestUnitBar', 'CheckUnitFoo')),
    ('TestUn?tBar Check*', ('TestUnitBar', 'CheckUnitFoo')),
    ('Test', ('TestUnitFoo', 'TestUnitBar')),
    ('Test*', ('TestUnitFoo', 'TestUnitBar')),
    ('*Foo', ('TestUnitFoo', 'CheckUnitFoo')),
    ('*Unit[!B]*', ('TestUnitFoo', 'CheckUnitFoo')),
    ('*Baz*', ()),
])
def test(testdir, option_value, expected_unittests):
    if option_value is not None:
        testdir.makeini("""
            [pytest]
            python_unittest_classes = {}
        """.format(option_value))
    items = testdir.getitems("""
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
    collected = sorted(item.nodeid.split('::')[1] for item in items)
    assert 'TestPytestFoo' in collected
    assert 'test_plain' in collected
    collected.remove('TestPytestFoo')
    collected.remove('test_plain')
    assert collected == sorted(expected_unittests)
