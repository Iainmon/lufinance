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
        "appdirs==1.4.4",
        "beautifulsoup4==4.9.3",
        "bs4==0.0.1",
        "certifi==2021.5.30",
        "chardet==4.0.0",
        "charset-normalizer==2.0.4; python_version >= '3.0'",
        "cssselect==1.1.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "fake-useragent==0.1.11",
        "feedparser==6.0.8; python_version >= '3.6'",
        "idna==3.2; python_version >= '3.0'",
        "lxml==4.6.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "multitasking==0.0.9",
        "numpy==1.21.1",
        "pandas==1.3.1",
        "parse==1.19.0",
        "pyee==8.1.0",
        "pyppeteer==0.2.5; python_version < '4' and python_full_version >= '3.6.1'",
        "pyquery==1.4.3",
        "python-dateutil==2.8.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pytz==2021.1",
        "requests-html==0.10.0; python_version >= '3.6'",
        "sgmllib3k==1.0.0",
        "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "soupsieve==2.2.1; python_version >= '3.0'",
        "tqdm==4.62.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "urllib3==1.26.6; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
        "w3lib==1.22.0",
        "websockets==8.1; python_full_version >= '3.6.1'",
        "yahoo-fin==0.8.9.1",
        "yfinance==0.1.63",
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
