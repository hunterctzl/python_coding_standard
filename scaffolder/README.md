# scaffolder

==============================

This repository contains code scaffolding projects using different templates

## Installation
The scaffolder package is pip installable. You can install this package in a virtual environment

### Virtual Environment
Developers are required to setup a venv for development
1. Go to the root of the repo, run `python3 -m venv my-venv` (you can use a different name).
2. If you are using PyCharm, go to Project, project name. | Python Interpreter, click Add Interpreter, browse for the desired Python executable (for example, /my-venv/bin/python)
3. If you are using command line, run `source my-venv/bin/activate`
4. To delete the venv, run `rm -r my-venv`

Local install:
From the root of the repo (i.e. if you type 'ls' you should see 'setup.py') run
```nohighlight
 pip install .
```

--------

Usage of the module
------------
Once you install the package using the above command, 
choose one template from the below available template list, 
and run the following command in terminal

```nohighlight
scaffold -t <template_name>>
```
Available template list: 
1. ds-template

Template detail:
1. ds-template is a template for Ml model project

The default template is ds-template

--------

