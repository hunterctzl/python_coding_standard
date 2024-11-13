"""
setup project for pip install
"""
from setuptools import find_packages
from setuptools import setup

base = [
    "pyspark==3.5.3",
    "pandas==2.2.3",
]
dev = [
    "pre-commit==4.0.1",
    "pytest==8.3.3",
    "pytest-cov==6.0.0",
    "pytest-mock==3.14.0",
    "pylint==3.3.1",
    "pdoc3==0.11.1",
]
prod = []

setup(
    name="package_template",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version="0.0.1",
    description="This is a template for DS projects",
    author="Le Zhang",
    install_requires=base,
    extras_require={
        "dev": dev,
        "prod": prod,
    },
)
