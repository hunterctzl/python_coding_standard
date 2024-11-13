import os

from setuptools import find_packages
from setuptools import setup

base = [
    "cookiecutter==1.7.3",
    "urllib3==1.26.6",
]

dev = []
prod = []


def recursive_get_package_data():
    matches = []
    THIS_FILE_DIR = os.path.dirname(os.path.realpath(__file__))
    THIS_FILE_DIR = os.path.join(THIS_FILE_DIR, "scaffolder")
    for root, dirnames, filenames in os.walk(THIS_FILE_DIR):
        for filename in filenames:
            matches.append(os.path.join(os.path.relpath(root, THIS_FILE_DIR), filename))

    return matches


setup(
    name="scaffolder",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={"scaffolder": recursive_get_package_data()},
    include_package_data=True,
    version="0.0.1",
    description="project generator",
    author="Le Zhang",
    install_requires=base,
    entry_points={
        "console_scripts": ["scaffold = scaffolder.generator:main"],
    },
)
