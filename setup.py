# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)

reqs = [str(ir.req) for ir in install_reqs]

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('scvid/scvid.py').read(),
    re.M
).group(1)


with open("scvid/README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name="scvid-lin",
    packages=["scvid"],
    entry_points={
        "console_scripts": ['scvid = scvid.scvid:main']
    },
    version=version,
    install_requires=reqs,
    description="Python command line application for creating video from live sceenshots.",
    long_description=long_descr,
    author="Serhii Dubovyk",
    author_email="sergeydubovick@gmail.com",
    url="https://github.com/dubovyk/scvid/",
)
