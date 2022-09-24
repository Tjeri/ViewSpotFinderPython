from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from mesh import find_view_spots


def read_json(file_path: Path) -> dict[str, Any]:
    with open(file_path) as json_file:
        return json.load(json_file)


def validate_and_parse_args() -> tuple[Path, int]:
    """
    Validates expected arguments and parses them

    Expect a valid file path and an integer. Raise errors otherwise.
    """
    if len(sys.argv) < 3:
        raise ValueError('Wrong number of arguments. Need: <file name> and <number of view spots>.')
    path = validate_and_parse_path(sys.argv[1])
    amount = validate_and_parse_amount(sys.argv[2])
    return path, amount


def validate_and_parse_path(path_str: str) -> Path:
    path = Path(path_str)
    if not path.exists() or not path.is_file():
        raise ValueError(f'"{path_str}" is not a valid file path')
    return path


def validate_and_parse_amount(amount: str | int) -> int:
    try:
        return int(amount)
    except ValueError as e:
        raise ValueError(f'"{amount}" is not a valid number.') from e


def read_and_print_view_spots() -> None:
    """
    Get json file and amount of view spots to show, find the view spots and print them in the required output format.
    """
    path, amount = validate_and_parse_args()
    sorted_spots = find_view_spots(read_json(path), amount)
    object_strings = [f'\t{{element_id: {element.id}, value: {element.height}}}' for element in sorted_spots]
    separator = ',\n'
    print(f'[\n{separator.join(object_strings)}\n]')


def aws_find_view_spots(data, context):
    if 'path' not in data:
        return build_error_response('Path is missing from data.')
    if 'amount' not in data:
        return build_error_response('Amount is missing from data.')
    try:
        path = validate_and_parse_path(data['path'])
        amount = validate_and_parse_amount(data['amount'])
    except ValueError as e:
        return build_error_response(str(e))
    sorted_spots = find_view_spots(read_json(path), amount)

    return {
        'statusCode': 200,
        'contentType': 'application/json',
        "body": json.dumps([{'element_id': element.id, 'value': element.height} for element in sorted_spots])
    }


def build_error_response(message: str) -> dict[str, Any]:
    return {
        'statusCode': 400,
        'body': f"{'message': {message}}"
    }


if __name__ == '__main__':
    read_and_print_view_spots()
