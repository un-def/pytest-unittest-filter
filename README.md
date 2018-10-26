# pytest-unittest-filter

[![Build Status](https://img.shields.io/travis/un-def/pytest-unittest-filter.svg?style=flat-square)](https://travis-ci.org/un-def/pytest-unittest-filter) [![PyPI](https://img.shields.io/pypi/v/pytest-unittest-filter.svg?style=flat-square&colorB=brightgreen)](https://pypi.org/project/pytest-unittest-filter/)

A pytest plugin for filtering unittest-based test classes


## Description

`pytest` has `unittest`-based tests [support out of the box][pytest-docs-unittest]. It eases incremental transition from legacy test suite to `pytest` for existing projects, but it has one drawback: there is no way to exclude some test cases (`unittest.TestCase` subclasses) from collection. `pytest` has `python_classes` [config option][pytest-docs-python-classes-option], but, as noted in documentation, this option doesn't affect `unittest.TestCase` subclasses:

> Note that unittest.TestCase derived classes are always collected regardless of this option, as unittest‘s own collection framework is used to collect those tests.

It's probably OK for projects that uses builtin `unittest` test runner (`python -m unittest`) because the latter has no any include/exclude option either, but it can be inconvenient if a project test suite is used with `nose` test runner and relies on [hard-coded][nose-src-underscore-exclude] leading underscore filter.

This plugin provides a new config option `python_unittest_classes` that works like the `python_classes` option mentioned above but for `unittest.TestCase` subclasses:

> One or more name prefixes or glob-style patterns determining which classes are considered for test collection. Search for multiple glob patterns by adding a space between patterns.

A default value is _none_ (no value), i.e. all `unittest.TestCase` subclasses are collected by default.


## Examples

* to exclude classes those names start with underscore:

```ini
[pytest]
python_unittest_classes = [!_]*
```

* to include only classes those names start with `Test` or `Check`:

```ini
[pytest]
python_unittest_classes = Test* Check*
```

or alternatively:

```ini
[pytest]
python_unittest_classes = Test Check
```

* to include only classes those names end with `TestCase`:

```ini
[pytest]
python_unittest_classes = *TestCase
```


## License

[MIT License][license]



[pytest-docs-unittest]: https://docs.pytest.org/en/latest/unittest.html
[pytest-docs-python-classes-option]: https://docs.pytest.org/en/latest/reference.html#confval-python_classes
[nose-src-underscore-exclude]: https://github.com/nose-devs/nose/blob/b3a505071d6de526d470218d310019d04280b69c/nose/selector.py#L66
[license]: https://github.com/un-def/pytest-unittest-filter/blob/master/LICENSE
