#!/usr/bin/env python
from setuptools import setup, find_packages

reqs = [
    'aiohttp==3.8.5',
    'astroid==1.5.3',
    'async-timeout==2.0.0',
    'Cerberus==1.1',
    'certifi==2017.11.5',
    'chardet==3.0.4',
    'colorama==0.3.9',
    'discord==0.0.2',
    'discord.py==0.16.12',
    'flake8==3.5.0',
    'future==0.16.0',
    'idna==2.6',
    'imgurpython==1.1.7',
    'isort==4.2.15',
    'lazy-object-proxy==1.3.1',
    'mccabe==0.6.1',
    'mongo==0.2.0',
    'multidict==3.3.2',
    'oauthlib==2.0.6',
    'pycodestyle==2.3.1',
    'pyflakes==1.6.0',
    'pylint==1.7.4',
    'pymongo==3.5.1',
    'python-twitter==3.3',
    'requests==2.18.4',
    'requests-oauthlib==0.8.0',
    'six==1.11.0',
    'SQLAlchemy==1.1.15',
    'urllib3==1.22',
    'websockets==3.4',
    'wrapt==1.10.11',
    'yarl==0.13.0'
]

setup(name='rolz-bot',
      version='1.0',
      description='Rolz.org discord bot',
      author='Igor Velme',
      author_email='ivelme@yandex.ru',
      url='http://space-walross.ml',
      packages=find_packages(),
      install_requires=reqs
      )
