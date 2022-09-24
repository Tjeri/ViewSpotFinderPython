from typing import Any
from unittest import TestCase

from mesh import find_view_spots


class MeshTestCase(TestCase):
    def build_simple_data(self, height_0: float, height_1: float, height_2: float) -> dict[str, Any]:
        # 3 triangles, all connected
        return {
            'elements': [
                {'id': 0, 'nodes': [0, 1, 2]},
                {'id': 1, 'nodes': [0, 1, 3]},
                {'id': 2, 'nodes': [1, 2, 4]},
            ],
            'values': [
                {'element_id': 0, 'value': height_0},
                {'element_id': 1, 'value': height_1},
                {'element_id': 2, 'value': height_2},
            ]
        }

    def build_advanced_data(self, height_0: float, height_1: float, height_2: float, height_3: float,
                            height_4: float) -> dict[str, Any]:
        # 5 triangles, 1, 2, 3 around 0, 4 above 3 (connected to 0, 1, 3)
        return {
            'elements': [
                {'id': 0, 'nodes': [0, 1, 2]},
                {'id': 1, 'nodes': [0, 1, 3]},
                {'id': 2, 'nodes': [1, 2, 4]},
                {'id': 3, 'nodes': [0, 2, 5]},
                {'id': 4, 'nodes': [0, 5, 6]},
            ],
            'values': [
                {'element_id': 0, 'value': height_0},
                {'element_id': 1, 'value': height_1},
                {'element_id': 2, 'value': height_2},
                {'element_id': 3, 'value': height_3},
                {'element_id': 4, 'value': height_4},
            ]
        }

    def build_line_data(self, height_0: float, height_1: float, height_2: float, height_3: float,
                        height_4: float) -> dict[str, Any]:
        # 5 triangles in a straight line. 2 connected to every other triangle.
        return {
            'elements': [
                {'id': 0, 'nodes': [0, 1, 2]},
                {'id': 1, 'nodes': [1, 2, 3]},
                {'id': 2, 'nodes': [1, 3, 4]},
                {'id': 3, 'nodes': [3, 4, 5]},
                {'id': 4, 'nodes': [4, 5, 6]},
            ],
            'values': [
                {'element_id': 0, 'value': height_0},
                {'element_id': 1, 'value': height_1},
                {'element_id': 2, 'value': height_2},
                {'element_id': 3, 'value': height_3},
                {'element_id': 4, 'value': height_4},
            ]
        }

    def get_view_spots(self, data: dict[str, Any], amount: int) -> list[tuple[int, float]]:
        return [(element.id, element.height) for element in find_view_spots(data, amount)]

    def test_ascending(self) -> None:
        data = self.build_simple_data(0, 1, 2)
        self.assertEqual([(2, 2)], self.get_view_spots(data, 3))

    def test_descending(self) -> None:
        data = self.build_simple_data(2, 1, 0)
        self.assertEqual([(0, 2)], self.get_view_spots(data, 3))

    def test_all_equal(self) -> None:
        data = self.build_simple_data(0, 0, 0)
        self.assertEqual([(0, 0)], self.get_view_spots(data, 3))

    def test_2_view_spots(self) -> None:
        data = self.build_advanced_data(0, 1, 3, 2, 4)
        self.assertEqual([(4, 4), (2, 3)], self.get_view_spots(data, 5))

    def test_2_view_spots_with_equality(self) -> None:
        data = self.build_advanced_data(0, 1, 3, 3, 4)
        self.assertEqual([(4, 4), (2, 3)], self.get_view_spots(data, 5))

    def test_advanced_1_view_spot(self) -> None:
        data = self.build_advanced_data(4, 3, 2, 1, 0)
        self.assertEqual([(0, 4)], self.get_view_spots(data, 5))

    def test_line_going_down(self) -> None:
        data = self.build_line_data(4, 3, 2, 1, 0)
        self.assertEqual([(0, 4)], self.get_view_spots(data, 5))

    def test_line_going_down_with_plateau(self) -> None:
        data = self.build_line_data(4, 3, 3, 3, 2)
        self.assertEqual([(0, 4), (3, 3)], self.get_view_spots(data, 5))

    def test_line_double_plateau(self) -> None:
        data = self.build_line_data(4, 4, 0, 3, 3)
        self.assertEqual([(0, 4), (4, 3)], self.get_view_spots(data, 5))

    def test_line_all_equal(self) -> None:
        data = self.build_line_data(4, 4, 4, 4, 4)
        self.assertEqual([(0, 4)], self.get_view_spots(data, 5))

    def test_line_interrupted_plateau(self) -> None:
        data = self.build_line_data(4, 4, 0, 4, 4)
        self.assertEqual([(0, 4)], self.get_view_spots(data, 5))

    def test_line_interrupted_plateau_2(self) -> None:
        data = self.build_line_data(3, 4, 0, 4, 4)
        self.assertEqual([(1, 4)], self.get_view_spots(data, 5))
