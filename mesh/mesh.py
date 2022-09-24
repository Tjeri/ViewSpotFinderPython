from typing import Any

from mesh.element import Element


def find_view_spots(jdon_data: dict[str, Any], amount: int) -> list[Element]:
    elements: dict[int, Element] = {element['element_id']: Element(element['element_id'], element['value'])
                                    for element in jdon_data['values']}
    nodes: dict[int, list[int]] = dict()
    for _element in jdon_data['elements']:
        element = elements[_element['id']]
        for node_id in _element['nodes']:
            neighbor_ids = nodes.setdefault(node_id, list())
            for neighbor_id in neighbor_ids:
                neighbor = elements[neighbor_id]
                if neighbor.height > element.height:
                    element.is_view_spot = False
                elif element.height > neighbor.height:
                    neighbor.is_view_spot = False
                else:
                    neighbor.add_plateau_neighbor(element)
            neighbor_ids.append(element.id)
    result = list()
    for element in sorted(elements.values(), key=lambda element: element.height, reverse=True):
        if element.is_view_spot:
            result.append(element)
            if len(result) >= amount:
                return result
            for neighbor in element.plateau_neighbors:
                neighbor.is_view_spot = False
    return result
