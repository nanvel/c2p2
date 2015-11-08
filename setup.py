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


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name="c2p2",
    version='0.0.2',
    description="Code Commit Push Publish blogging/docs engine.",
    long_description=read('README.md'),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='tornado, github, blog, publish',
    author='Oleksandr Polieno',
    author_email='polyenoom@gmail.com',
    url="https://github.com/nanvel/c2p2",
    packages=find_packages(),
    install_requires=[
        'tornado==4.2',
        'Markdown==2.6.2',
        'Pygments==2.0.2',
        'arrow==0.6.0',
        'python-slugify==1.1.3',
        'ipaddress==1.0.14',
    ]
)
