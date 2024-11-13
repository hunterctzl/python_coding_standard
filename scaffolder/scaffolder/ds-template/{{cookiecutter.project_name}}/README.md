# {{cookiecutter.project_name}}

==============================

This template for DS projects.
Feel free to modify the structure to better fit your project.

Recommendation keeping these files:
- Keep README.md in the root path
- Keep setup.py in the root path to make your project pip installable. 

This repository contains code of {{cookiecutter.project_name}}

Project Organization
------------

```nohighlight
├── README.md                     <- The top-level README for developers using this project.
│
├── assets                        <- Generated analysis as HTML, LaTeX, etc.
│
├── data
│   ├── external                  <- Data from third party sources.
│   ├── interim                   <- Intermediate data that has been transformed.
│   ├── processed                 <- The final, canonical data sets for modeling.
│   └── raw                       <- The original, immutable data dump.
│
├── models                        <- The model files.
│
├── docs                          <- The documentation files.
│
├── notebooks                     <- Jupyter notebooks. 
│   │
│   ├── extract                   <- Notebook examples to use extract classes/functions.
│   ├── eda                       <- Notebook for Explorative Data Analysis and your understanding of data.
│   ├── evaluation                <- Notebook examples to use evaluation classes/functions.
│   ├── preprocessing             <- Notebook examples to use preprocessing classes/functions.
│   ├── postprocessing            <- Notebook examples to use postprocessing classes/functions.
│   ├── load                      <- Notebook examples to use load classes/functions.
│   ├── transform                 <- Notebook examples to use transform classes/functions.
│   ├── models                    <- Notebook examples to use models classes/functions.
│   └── pipeline                  <- Notebook examples to use pipeline classes/functions.
│
│
├── setup.py                      <- Make this project pip installable with `pip install -e`.
│
├── {{cookiecutter.package_name}} <- Source code for use in this project.
│   ├── __init__.py               <- Makes src a Python module.
│   ├── extract                   <- The data extraction module.
│   ├── evaluation                <- The evaluation module.
│   ├── preprocessing             <- The preprocessing module.
│   ├── load                      <- The data loading module.
│   ├── transform                 <- The data transform module.
│   ├── models                    <- The modeling module.
│   ├── pipeline                  <- The pipeline module.
│   ├── postprocessing            <- The postprocessing module.
│   └── utils                     <- The utils code.
│
└── tests                         <- The unit test code; the structure must follow the source code.
```


--------


## Installation
The {{cookiecutter.project_name}} package is pip installable. The easiest way is to
1. clone the repo to your machine
2. from the root of the repo (i.e. if you type `ls` you should see `setup.py`) run `pip install .`
3. For development purpose, run `pip install -e ".[dev]"` to install extra required packages.  

## Virtual Environment
Developers are required to setup a venv for development
1. Go to the root of the repo, run `python3 -m venv my-venv` (you can use a different name).
2. If you are using PyCharm, go to Project, project name. | Python Interpreter, click Add Interpreter, 
browse for the desired Python executable (for example, /my-venv/bin/python)
3. If you are using command line, run `source my-venv/bin/activate`
4. Run `pip install -e ".[dev]"`
5. Run `pytest --cov-report term-missing --cov={{cookiecutter.package_name}} tests/`
6. To delete the venv, run `rm -r my-venv` 

## pytest 
The pytest is a framework to write small tests to support functional testing for python applications and libraries. 
It can be easily scaled to support compile functional test. 
For more information, refer to https://docs.pytest.org/en/stable
1. Run `pip install pytest` and `pip install pytest-cov` in your venv.
2. Run `pytest --cov-report term-missing --cov={{cookiecutter.package_name}} tests/` to see coverage and missing lines. 

## pylint
The pylint analyze your code without actually running it. 
It checks for error, enforces a coding standard, looks for code smells, 
and can make suggestions about how the code could be refactored. 
1. Run `pip install pylint` in your venv.
2. Run `pylint --rcfile=.pylintrc {{cookiecutter.package_name}}` to see pylint report. 

## black
Black scans all files and formats your Python code in PEP 8 style in place.
1. Run `pip install black` in your venv (optional, if you haven't installed it).
2. Run `black {source_file_or_directory}` (black will format your Python code in place). 

## pre-commit
One good practice is to use pre-commit to check the code quality. 
It uses .pre-commit-config.yaml to apply rules to your code whe you do git commit.
Here are some steps to help you setup pre-commit:
1. If not yet install pre-commit, do `pip install pre-commit`.
2. In terminal, go to the root of the repo
3. Run `pre-commit install`.
4. Run `pre-commit run --all-files`.
5. Next time when you commit your code, the pre-commit will check:
- Check for added large
- Don't commit to branch
- Check merge conflict
- Reorder python imports
- Trailing whitespace
- black
- blacken-docs
- pylint
- pytest

## Numpy Docstring
A documentation string (docstring) is a documentation that describes a module, function, class, or method definition. 
The docstring is a spacial attribute of the object (`object.__doc__`) and, for consistency, 
is surrounded by triple double quotes, i.e.:
```
"""This is the form of a docstring.
It can be spread over several lines.
"""
```
Numpy, SciPy, and the scikit-learn follow a common convention for docstrings that provides for consistency,
while also allowing our toolchain to produce well-formatted reference guides.
For more information, refer to https://numpydoc.readthedocs.io/en/latest/format.html
### Setup Numpy Docstring in PyCharm
1. PyCharm -> Preferences -> Python Integrated Tools.
2. In Docstring format dropdown - choose Numpy. Click Apply and Ok.
3. Type `""""""` and Enter to generate Numpy docstrings in your code.py and test_code.py within PyCharm. 
One in the top of your file, one in each class, and one in each method is recommended. 
By default IDE generates parameters and returns, feel free to add examples and raises 
(if exception is expected to be raised)

## pdoc
pdoc provides command-line interface for converting docstring into a documentation html file.
- Write a docstring in `__init__.py` for a very high-level overview of that submodule.
- Write a docstring AT THE VERY TOP of `my_function.py` for high-level overview of its contents..
- Write a docstring AT THE VERY TOP of every class or function you wish to document.
this count/should be low-level explanation (for this we are using Numpy doc style). 
1. Install pdoc in your environment: `pip install pdoc3` (notice the 3 at the end).
2. Run `pdoc --http 0.0.0.0:8080 --skip-errors repo_name/` (replace repo_name with your repo name)
3. Open a web browser, and go to `http://localhost:8080/`, and admire the doc pages in all their glory.
4. Use pdoc to generate html files: `pdoc --html --force -o docs --skip-errors repo_name/` 
(replace repo_name with your repo name). pdoc will create a folder called docs which will contain the generated html. 