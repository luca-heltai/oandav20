import sys
from setuptools import setup, find_packages

import pypandoc

if sys.version_info < (3, 5, 0):
    sys.exit("ERROR: You need Python 3.5 or later to use oandav20.")

long_description = pypandoc.convert("README.md", "rst")

setup(
    name="oandav20",
    version="0.2.0",
    description="Unofficial SDK for Oanda v20 REST API.",
    long_description=long_description,
    author="Nait Aul",
    author_email="nait-aul@protonmail.com",
    url="https://github.com/nait-aul/oandav20",
    licence="MIT License",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries",
    ]
)
