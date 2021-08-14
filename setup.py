#!/usr/bin/env python
#
# Lufrano Financial Instrument Library
# Copyright Iain Moncrief 2021
#


"""Lufrano Financial Instrument Library"""

from setuptools import setup, find_packages
import io
from os import path

version = "unknown"
with open("lufinance/version.py") as fi:
    line = fi.read().strip()
    version = line.replace("version = ", "").replace('"', "")


here = path.abspath(path.dirname(__file__))

# # Get the long description from the README file
# with io.open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#     long_description = f.read()

setup(
    dependency_links=[
        "git+https://github.com/requests/requests.git@b0e025ade7ed30ed53ab61f542779af7e024932e#egg=requests"
    ],
    install_requires=[
        "certifi==2021.5.30",
        "charset-normalizer==2.0.4; python_version >= '3'",
        "idna==3.2; python_version >= '3.5'",
        "urllib3==1.26.6; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
    ],
    name="lufinance",
    version=version,
    description="Financial instrument library",
    long_description="",
    url="https://github.com/iainmon/lufinance",
    author="Iain Moncrief",
    author_email="iainmoncrief@gmail.com",
    license="Copyright",
    classifiers=[
        # 'License :: Copyright',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    platforms=["any"],
    keywords="pandas, finance",
    packages=find_packages(exclude=[]),
    # install_requires=['pandas>=0.24', 'numpy>=1.15',
    #                   'requests>=2.20', 'multitasking>=0.0.7',
    #                   'lxml>=4.5.1'],
    entry_points={"console_scripts": ["sample=sample:main",],},
)
