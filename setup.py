import sys
import zdict

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

zdict.utils.create_zdict_dir_if_not_exists()
zdict.utils.create_zdict_db_if_not_exists()


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

requires = [
    'beautifulsoup4',
    'peewee',
    'requests',
]

if sys.platform == 'darwin' and sys.version_info < (3, 5):
    requires.append('gnureadline')


setup(
    packages=find_packages(exclude=['scripts']),
    scripts=['scripts/zdict'],
    install_requires=requires,
    tests_require=['coverage', 'pytest', 'pytest-cov', 'gnureadline'],
    cmdclass={'test': PyTest},

    name='zdict',
    version=zdict.__version__,
    author='Shun-Yi Jheng',
    author_email='M157q.tw@gmail.com',
    maintainer='Shun-Yi Jheng, Iblis Lin, Chang-Yen Chih, Chiu-Hsiang Hsu',
    maintainer_email=('M157q.tw@gmail.com,'
                      'e196819@hotmail.com,'
                      'michael66230@gmail.com,'
                      'wdv4758h@gmail.com'),
    url='https://github.com/zdict/zdict',
    keywords="cli, dictionary, framework",
    description="The last dictionary framework you need. (?)",
    long_description="zdict is a CLI dictionay framework mainly focus on any kind of online dictionary.",
    download_url="https://github.com/zdict/zdict/archive/v{}.zip".format(zdict.__version__),
    platforms=['Linux', 'Mac'],
    license="GPL3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: Chinese (Traditional)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
    ],
)
