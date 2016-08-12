import sys
from setuptools import setup, find_packages

import oandav20

if sys.version_info < (3, 5, 0):
    sys.exit("ERROR: You need Python 3.5 or later to use oandav20.")

setup(
    name="oandav20",
    version=oandav20.__version__,
    description="Unofficial Oanda v20 REST API wrapper.",
    long_description="",  # TODO
    author="Nait Aul",
    author_email="nait-aul@protonmail.com",
    url="https://github.com/nait-aul/oandav20",
    licence="MIT License",
    packages=find_packages(),
    install_requires=["requests>=2.10.0"],
    classifiers="",
)
