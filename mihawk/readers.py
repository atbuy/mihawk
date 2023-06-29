from typing import Generator
from xml.dom import minidom

from mihawk.models import Point


class KMLReader:
    def __init__(self, file: str):
        # Parse open KML file.
        # The caller is responsible for closing the file.
        dom = minidom.parse(file)
        names = dom.getElementsByTagName("name")
        coordinates = dom.getElementsByTagName("coordinates")

        coords = []
        for coord, name in zip(coordinates, names):
            coordinates = coord.firstChild.nodeValue
            name = name.firstChild.nodeValue
            values = self._clean_coords(coordinates)
            point = Point(*values, name=name)
            coords.append(point)

        self.points = coords

    def _clean_coords(self, text: str) -> Generator[float, None, None]:
        """Clean coordinates from KML file."""

        coordinates = text.split(",")
        return (float(coord) for coord in coordinates)
