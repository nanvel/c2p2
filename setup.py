# -*- encoding: utf-8 -*-
"""
Python setup file for the nicedit app.

In order to register your app at pypi.python.org, create an account at
pypi.python.org and login, then register your new app like so:

    python setup.py register

If your name is still free, you can now make your first release but first you
should check if you are uploading the correct files:

    python setup.py sdist

Inspect the output thoroughly. There shouldn't be any temp files and if your
app includes staticfiles or templates, make sure that they appear in the list.
If something is wrong, you need to edit MANIFEST.in and run the command again.

If all looks good, you can make your first release:

    python setup.py sdist upload

For new releases, you need to bump the version number in
tornado_botocore/__init__.py and re-run the above command.

For more information on creating source distributions, see
http://docs.python.org/2/distutils/sourcedist.html

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
