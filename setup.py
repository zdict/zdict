from setuptools import find_packages, setup

import zdict

zdict.utils.create_zdict_dir_if_not_exists()
zdict.utils.create_zdict_db_if_not_exists()

EXCLUDE_FROM_PACKAGES = ['scripts']

setup(
    name='zdict',
    version=zdict.__version__,
    description='The last dictionary framework you will need. (?)',
    author='Shun-Yi Jheng',
    author_email='M157q.tw@gmail.com',
    maintainer='Iblis Lin, Chang-Yen Chih, Chiu-Hsiang Hsu',
    maintainer_email='e196819@hotmail.com, michael66230@gmail.com, wdv4758h@gmail.com',
    url='https://github.com/M157q/zdict',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    scripts=['scripts/zdict'],
    install_requires=[
        'beautifulsoup4',
        'peewee',
        'readline',
        'requests',
    ],
)
