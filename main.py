from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from mesh.mesh import find_view_spots


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
    path = Path(sys.argv[1])
    if not path.exists() or not path.is_file():
        raise ValueError(f'"{sys.argv[1]}" is not a valid file path')
    try:
        amount = int(sys.argv[2])
    except ValueError as e:
        raise ValueError(f'"{sys.argv[2]}" is not a valid number.') from e
    return path, amount


def read_and_print_view_spots() -> None:
    """
    Get json file and amount of view spots to show, find the view spots and print them in the required output format.
    """
    path, amount = validate_and_parse_args()
    sorted_spots = find_view_spots(read_json(path), amount)
    object_strings = [f'\t{{element_id: {element.id}, value: {element.height}}}' for element in sorted_spots]
    separator = ',\n'
    print(f'[\n{separator.join(object_strings)}\n]')


if __name__ == '__main__':
    read_and_print_view_spots()
