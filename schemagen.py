import os
import json
import codegen.codegen_utils as cg

PREAMBLE = """
import strawberry
from typing import Optional
"""

CONFIG_FILEPATH = 'config/codegen_config.json'

def generate_schema():
    config = get_obj_from_file(CONFIG_FILEPATH)

    from_responses = config['from_responses']

    for item in from_responses:
        generate_code_from_response(item.get('name'), item.get('input_file'), item.get('output_file'), exclude_fields=item.get('exclude_fields'))

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