"""
setup.py

Setup for installing the package.
"""
from setuptools import setup, find_packages
from pathlib import Path

import passlock

VERSION = passlock.__version__
AUTHOR = passlock.__author__
EMAIL = passlock.__email__

BASE_DIR = Path(__file__).resolve().parent
README = BASE_DIR.joinpath("README.md")

setup(
    name="passlock",
    version=VERSION,
    description="Password protect your sensitive files from prying eyes. (passlock)",
    long_description=README.read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/clamytoe/passlock",
    author=AUTHOR,
    author_email=EMAIL,
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        # How mature is this project? Common values are
        #   1 - Planning
        #   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        #   6 - Mature
        #   7 - Inactive
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="python utility",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=["pytest"],
    license="MIT",
    entry_points={
        "console_scripts": [
            "passlock=passlock.app:main"
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/clamytoe/passlock/issues',
        'Source': 'https://github.com/clamytoe/passlock/',
    },
)
