from setuptools import setup
from pip.req import parse_requirements

import ydict


setup(
    name='ydict',
    version=ydict.__version__,
    description='A CLI tool for Yahoo! dictionary (https://tw.dictionary.yahoo.com/) using Python 3',
    author='Shun-Yi Jheng',
    author_email='M157q.tw@gmail.com',
    maintainer='Iblis Lin',
    maintainer_email='e196819@hotmail.com',
    url='https://github.com/M157q/ydict',
    packages=['ydict'],
    scripts=['scripts/ydict'],
    install_requires=[str(i.req) for i in  parse_requirements('./requirements.txt')],
)
