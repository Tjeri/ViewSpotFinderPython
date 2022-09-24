from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

from mesh.mesh import find_view_spots


def read_json(file_path: Path) -> dict[str, Any]:
    with open(file_path) as json_file:
        return json.load(json_file)


def read_and_print_view_spots():
    sorted_spots = find_view_spots(read_json(Path(sys.argv[1])), int(sys.argv[2]))
    object_strings = [f'\t{{element_id: {element.id}, value: {element.height}}}' for element in sorted_spots]
    separator = ',\n'
    print(f'[\n{separator.join(object_strings)}\n]')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise ValueError('Wrong number of arguments. Need: <file name> and <number of view spots>.')
    path = Path(sys.argv[1])
    if not path.exists():
        raise ValueError(f'"{path}" does not exist.')
    start = time.time()
    read_and_print_view_spots()
    print(time.time() - start)
