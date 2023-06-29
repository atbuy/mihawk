from typing import Generator
from xml.dom import minidom

from mihawk.models import Point


class KMLReader:
    def __init__(self, file: str):
        # Parse open KML file.
        # The caller is responsible for closing the file.
        dom = minidom.parse(file)
        coordinates = dom.getElementsByTagName("coordinates")

        coords = []
        for coord in coordinates:
            text = coord.firstChild.nodeValue
            values = self._clean_coords(text)
            point = Point(*values)
            coords.append(point)

        self.points = coords

    def _clean_coords(self, text: str) -> Generator[float]:
        """Clean coordinates from KML file."""

        coordinates = text.split(",")
        cleaned = (float(coord) for coord in coordinates)
        return cleaned
