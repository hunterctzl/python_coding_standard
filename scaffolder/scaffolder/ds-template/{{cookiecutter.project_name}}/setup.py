"""
setup project for pip install
"""
from setuptools import find_packages
from setuptools import setup

base = [
    "numpy==1.20.3",
    "pandas==1.1.3",
    "scipy==1.4.1",
    "scikit-learn==0.24.1",
]
dev = [
    "blacken-docs=1.19.1",
    "pre-commit==2.9.2",
    "pytest==7.2.2",
    "pytest-cov==4.0.0",
    "pytest-mock==3.6.1",
    "pylint==2.17.4",
    "pytest-sonarjson==1.0.6",
    "pdoc3==0.10.0",
]
prod = []

setup(
    name="{{cookiecutter.package_name}}",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version="0.0.1",
    description="{{cookiecutter.description}}",
    author="{{cookiecutter.author}}",
    install_requires=base,
    extras_require={
        "dev": dev,
        "prod": prod,
    },
)
