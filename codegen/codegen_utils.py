from utils.casing import camel_to_snake

def response_to_schema(obj: dict, class_name: str, exclude_fields: list[str] = []) -> str:
    # start with class header
    result = f"@strawberry.type\nclass {class_name}:\n"

    # add attributes
    for key, value in obj.items():
        if key in exclude_fields: continue

        # if the value is a nested object, we will need to create another class for it
        attribute_name = camel_to_snake(key)
        type_name = type(value).__name__

        if type_name == 'dict':
            subclass_name = f'{class_name}{key[0].upper()}{key[1:]}'
            result += f'\t{attribute_name}: Optional[{subclass_name}] = None\n'

            # generate the subclass recursively and prepend it to the current result
            result = response_to_schema(value, subclass_name, exclude_fields) + '\n' + result
        else:
            result += f'\t{attribute_name}: Optional[{type_name}] = None\n'

    return result
