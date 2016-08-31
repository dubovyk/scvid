# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('scvid.py').read(),
    re.M
).group(1)


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name="scvid-lin",
    packages=["scvid"],
    entry_points={
        "console_scripts": ['scvid = scvid:main']
    },
    version=version,
    description="Python command line application for creating video from live sceenshots.",
    long_description=long_descr,
    author="Serhii Dubovyk",
    author_email="sergeydubovick@gmail.com",
    url="",
)
