import argparse
import pathlib
from os import path

import cookiecutter.main as cmain
from cookiecutter.exceptions import RepositoryNotFound


def main():
    available_templates = ["ds-template"]
    parser = argparse.ArgumentParser(prog="scaffold")
    parser.add_argument("-t", default="ds-template", dest="template")
    args = parser.parse_args()
    template_to_generate = args.template
    if template_to_generate in available_templates:
        file_path = pathlib.Path(__file__).parent.resolve()
        template_path = path.join(file_path, template_to_generate)
        try:
            cmain.cookiecutter(template_path)
            print(f"Project for {template_to_generate} has been created successfully")
        except RepositoryNotFound as e:
            print(f"template not found, available templates are: {available_templates}")
    else:
        print(f"template not found, available templates are: {available_templates}")
