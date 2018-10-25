import os
import re
import codecs

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))


def read(file_name):
    file_path = os.path.join(here, file_name)
    with codecs.open(file_path, encoding='utf-8') as file_obj:
        return file_obj.read()


version = re.search(
    "__version__ = '([.0-9a-z]+)'",
    read('pytest_unittest_filter.py'),
).group(1)


setup(
    name='pytest-unittest-filter',
    version=version,
    author='un.def',
    author_email='me@undef.im',
    license='MIT',
    url='https://github.com/un-def/pytest-unittest-filter',
    description='A pytest plugin for filtering unittest-based test classes',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    py_modules=['pytest_unittest_filter'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=['pytest>=3.1.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': ['unittest-filter = pytest_unittest_filter'],
    },
)
