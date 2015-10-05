import sys
import zdict

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

zdict.utils.create_zdict_dir_if_not_exists()
zdict.utils.create_zdict_db_if_not_exists()

EXCLUDE_FROM_PACKAGES = ['scripts']
REQUIRES = [
    'beautifulsoup4',
    'peewee',
    'requests',
]

try:
    import readline
except ImportError:
    REQUIRES += ['readline']


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='zdict',
    version=zdict.__version__,
    description='The last dictionary framework you will need. (?)',
    author='Shun-Yi Jheng',
    author_email='M157q.tw@gmail.com',
    maintainer='Iblis Lin, Chang-Yen Chih, Chiu-Hsiang Hsu',
    maintainer_email=('e196819@hotmail.com, '
                      'michael66230@gmail.com, '
                      'wdv4758h@gmail.com'),
    url='https://github.com/M157q/zdict',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    scripts=['scripts/zdict'],
    install_requires=REQUIRES,
    tests_require=['coverage', 'pytest'],
    cmdclass={'test': PyTest}
)
