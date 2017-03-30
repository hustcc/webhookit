# -*- coding: utf-8 -*-
import setuptools  # noqa
from distutils.core import setup
import io
import re
import os


DOC = '''
## 1. Install

> **pip install webhookit**

Then get cli command `webhookit_config` and `webhookit`.


## 2. Usage

Simple, like below:

> **webhookit_config > config.py**

> **webhookit -c config.py -p 18340**

Or you can `webhookit --help` to get the help content.
'''


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name='webhookit',
      version=find_version('webhookit/app.py'),
      description=('Bind git webhooks with actions. '
                   'Simple git webhook cli tool for automation tasks.'),
      long_description=DOC,
      author='hustcc',
      author_email='i@hust.cc',
      url='https://github.com/hustcc',
      license='MIT',
      install_requires=[
        'click',
        'tornado',
      ],
      classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities'
      ],
      keywords='webhookit, webhook, github, gitlab, gogs, git-webhook',
      include_package_data=True,
      zip_safe=False,
      packages=['webhookit'],
      entry_points={
        'console_scripts': [
          'webhookit=webhookit.cli:runserver',
          'webhookit_config=webhookit.cli:config'
        ]
      })
