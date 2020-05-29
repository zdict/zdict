import sys
import os

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))


def parse_requirements(filepath):
    """ load requirements from a pip requirements file. """
    with open(filepath) as f:
        lines = (line.strip() for line in f)
        return [line for line in lines if line and not line.startswith('#')]


def get_zdict_version():
    constants_file_path = os.path.join(ROOT_DIR, 'zdict/constants.py')
    with open(constants_file_path) as constants:
        for line in constants:
            if line.startswith('VERSION'):
                code = compile(line, '<string>', 'single')
                version = code.co_consts[0]

        return version


def get_test_req():
    test_requirements = parse_requirements(
        os.path.join(ROOT_DIR, 'requirements-test.txt')
    )

    if not sys.platform.startswith('freebsd'):
        test_requirements.append('gnureadline==6.3.3')

    return test_requirements


version = get_zdict_version()


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
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


install_requirements = parse_requirements(
    os.path.join(ROOT_DIR, 'requirements.txt')
)

if sys.platform == 'darwin' and sys.version_info <= (3, 5):
    install_requirements.append('gnureadline==6.3.3')


setup(
    packages=find_packages(exclude=['scripts']),
    scripts=['scripts/zdict'],
    install_requires=install_requirements,
    tests_require=get_test_req(),
    cmdclass={'test': PyTest},

    name='zdict',
    version=version,
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
    long_description=open("README.rst", encoding='utf-8').read(),
    download_url="https://github.com/zdict/zdict/archive/v{}.zip".format(
        version
    ),
    platforms=['Linux', 'Mac'],
    license="GPL3",
    python_requires=">=3, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: Chinese (Traditional)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ],
)
