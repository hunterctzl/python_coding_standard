# Python Coding Standard User Guide

# Summary
This project is to design the coding standard for Python projects.
The design is intended to solve the following challenges:
- Define a Python coding standard for naming convention, Python code format, line length, etc.
- Define a linter to check Python code quality.
- Define a Python framework for scalability and usablity.
- Define a standardized solution to setup Python environment for development.
- Define a unit test strategy to ensure test coverage (90%).
- Define Python docstring and documentation standard to improve the code readability.

# Terminology
## scaffolder
Complicated software projects often share certain conventions on 
project structure and requirements.
To simplify the creation of projects following those conventions,
"scaffolding" tools can automatically generate them at the beginning of each project.

## venv 
The venv Python module supports creating lightweight "virtual environments", 
each with their own independent set of Python packages installed in their site directories.
A virtual environment is created on top of an existing Python installation, 
known as the virtual environment's "base" Python,
and may optionally be isolated from the packages in the base environment, 
so only those explicitly installed in the virtual environment are available.

## pip install
PIP is a package management system used to install and manage software 
packages written in Python. It stands for "preferred installer program" or
"Pip Installs Packages." PIP for Python is a utility to manage
PyPI package installations from the command line.

## pytest
The pytest is a software test framework for Python code.
It is a command-line tool that automatically finds tests you've written, 
runs the tests, and reports the results.

## Docstring
A Python docstring is a string used to document a Python module, class, 
function or method, so programmers can understand what it does without 
having to read the details of the implementation.
Also, it is a common practice to generate online (html) documentation 
automatically from docstrings.

## pdoc
Pdoc is a software package for generating API documentation for 
Python programming Language, Pdoc uses introspection to extract 
documentation from source code docstrings and allows programmers 
to generate HTML documentation for chosen Python modules.

## PEP 8
PEP 8 is a document that provides guidelines and best practices on how to write Python code.

## pre-commit
A framework for managing and maintaining multi-Language pre-commit hooks.

## black
Black is a PEP 8 compliant opinionated formatter.
Black formats entire files in place.

## pylint
Pyint analyses your code without actually running it.
It checks for errors, enforces a coding standard, looks for code smells, 
and can make suggestions about how the code could be refactored.

# Interface Specification
- Follow [scaffolder-README,md](scaffolder/README.md) to use scaffold command to generate projects.
- Follow the [python coding-standard.md](python-coding-standard.md) to write python code,
- use pre-commit to check code quality when commit the code,
- use pytest and pylint to check test coverage and code quality.
# Implementation
There are 6 steps to implement this python coding stenderd;
## 1. Use the ds-template in scaffolder to generate a python project
Follow [scaffolder-READNE.md](scaffolder/README.md) to use scaffold command 
to generate a Python project using the python-template.
```
The scaffolder package is pip installable. Download the scaffolder file to your locat path 
Local install: From the root of the repo (i.e. if you type is you should see setup.py) run
    pip install
Once you install the package using the above command, run
    scaffold -t python-template
Follow the instruction to filt in project_name, package_name, description, and author for your python project.
```

The python-template pre-define the structure of an DS Python project, 
you can view the structure in [README.md](project-template/README.md).
The README.md, docs, script, package name, tests, setup.py are mandatory 
for a python project. You can modify other folders for your project.

## 2. Setup a virtual environment for development
Follow the [README.md](project-template/README.md) to setup venv,
run pip install and run pytest to ensure you successfully setup the environment for development.
It is mandatory to use a virtual environment for development because you need 
to install required packages for this project.

## 3. Following the Python coding standard to write code
Follow the [python coding-standard.md](python-coding-standard.md) to write
Python code in PEP8 style. It is mandatory to follow the Pthon coding standard.

## 4. Write unit test in pytest and ensure your test coverage
Follow the [test_reader_template.py](project-template/tests/extract/test_reader_template.py) 
to write unit tests in pytest.
And then follow the [README.md](project-template/README.md) to run pytest
and check coverage and missing lines.

## 5. Write docstring and use pdoc to generate documentation 
Follow the [README.md](project-template/README.md) to write numpy style docstring 
and use pdoc to generate documentation,
It is mandatory to write docstring for your code,

## 6. Use pre-commit to improve code quality
Before you commit your code, follow the [README.md](project-template/README.md) 
to run pre-commit to apply black to format your code, 
run pylint to check the quality of your code, 
and run pytest to test your code.
It is mandatory to pass all pre-commit hooks to commit your code.

# Rationale and alternatives
- Compare to other Linter, pylint provide a more comprehensive check, including
    - (C) convention, for programming standard violation
    - (R) refactor, for bad code smell
    - (W) warning, for python specific problems
    - (E) error, for probable bugs in the code
    - (F) fatal, if an error occurred which prevented pylint from doing

    However, pylint takes a long time to run, and it's the default output includes too much noise.
Thus, we use [Google pylint configuration](https://github.com/google/styleguide/blob/gh-pages/pylintrc) 
to optimize the pylint.

    The alternative is Flake. It's fast and has a low rate of false positives.
- venv is embedded in Python, it is lightweight and easy to use it.
The alternative couLd be conda virtual environment.
- pip install can be easily managed by setup.py, and it can be published in PyPI.
The alternative is conda install.
- pytest allows complex testing using less code, it supports unittest test suites. 
and it offers more than 800 external plugins. The alternative could be unittest.
- numpy docstring is widely used in DS projects, 
it is easy to share between DS teams and engineering teams.
It is compatible with pdoc and Sphinx, The alternative could be Google docstring.
- pdoc is a lightweight solution to generate Python project documentation.
The alternative could be sphinx,
