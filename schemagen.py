import os
import json
import codegen.codegen_utils as cg

PREAMBLE = """
import strawberry
from typing import Optional
"""

LEAGUE_FILEPATH = 'codegen/responses/league.json'
LEAGUE_OUTPUT = 'schema/league.py'

def generate_schema():
    generate_code_from_response("League", LEAGUE_FILEPATH, LEAGUE_OUTPUT, exclude_fields=['link', 'sport', 'sortOrder'])

def generate_code_from_response(class_name, response_filepath, output_filepath, preamble = f'{PREAMBLE.strip()}\n\n', exclude_fields = []):
    code = cg.response_to_schema(get_obj_from_file(response_filepath), class_name, exclude_fields)

    with open(output_filepath, 'w') as output:
        output.write(preamble + code)

def get_obj_from_file(filepath) -> dict:
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(f'{dir_path}/{filepath}') as file:
        obj = json.loads(file.read())

    return obj

if __name__ == '__main__':
    generate_schema()