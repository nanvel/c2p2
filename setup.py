"""
Python setup file for the c2p2 app.

For new releases, you need to bump the version number in
c2p2/__init__.py.

For testing:
python setup.py install

Upload to PyPI:
python setup.py bdist_wheel --universal
python setup.py sdist
twine upload dist/*
"""
import os

from setuptools import setup, find_packages

from c2p2 import VERSION


def read(file_name):
    try:
        return open(os.path.join(os.path.dirname(__file__), file_name)).read()
    except IOError:
        return ''


def parse_requirements():
    requirements_text = read(file_name='requirements.txt')
    return (line.strip() for line in requirements_text.split('\n') if '=' in line)


setup(
    name="c2p2",
    version=VERSION,
    description="Code Commit Push Publish engine.",
    long_description=read(file_name='README.rst'),
    license="The MIT License",
    platforms=['OS Independent'],
    keywords='tornado, github, blog, publish',
    author='Oleksandr Polieno',
    author_email='polyenoom@gmail.com',
    url='https://github.com/nanvel/c2p2',
    packages=find_packages(),
    install_requires=parse_requirements()
)
