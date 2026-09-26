import re
from typing import Any

_CAMEL_CASE_PATTERN = re.compile(r'(?<!^)(?=[A-Z])')


def camel_to_snake(value: str) -> str:
    """Converts a camelCase string to snake_case."""
    return _CAMEL_CASE_PATTERN.sub('_', value).lower()


def keys_to_snake_case(data: Any) -> Any:
    """Recursively converts camelCase dict keys (including nested dicts/lists) to snake_case."""
    if isinstance(data, dict):
        return {
            camel_to_snake(key): keys_to_snake_case(value)
            for key, value in data.items()
        }
    if isinstance(data, list):
        return [keys_to_snake_case(item) for item in data]

    return data
