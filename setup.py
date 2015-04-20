from setuptools import setup

import zdict


setup(
    name='zdict',
    version=zdict.__version__,
    description='The last dictionary framework you will need. (?)',
    author='Shun-Yi Jheng',
    author_email='M157q.tw@gmail.com',
    maintainer='Iblis Lin, Chang-Yen Chih, Chiu-Hsiang Hsu',
    maintainer_email='e196819@hotmail.com, michael66230@gmail.com, wdv4758h@gmail.com',
    url='https://github.com/M157q/zdict',
    packages=['zdict'],
    scripts=['scripts/zdict'],
    install_requires=[
        'beautifulsoup4',
        'requests',
        'peewee',
    ],
)
