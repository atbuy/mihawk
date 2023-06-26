from pathlib import Path
from unittest import TestCase

from mihawk.models import Point
from mihawk.readers import KMLReader


class TestReaders(TestCase):
    @classmethod
    def setUpClass(cls):
        # Read test data to use in each test
        cwd = Path(__file__).parent.absolute()
        test_file = cwd.joinpath("utils", "test.kml")
        with open(test_file) as file:
            cls.data = KMLReader(file)

    def test_point(self):
        """Check the coordinates of the first point."""

        point = self.data.coords[0]
        self.assertEqual(point.latitude, 24.4101949867021)
        self.assertEqual(point.longitude, 40.9409169808368)
        self.assertEqual(point.elevation, 61.735649)

    def test_point_distance(self):
        """Check the subtraction of two points."""

        point1 = Point(0, 1, 1)
        point2 = Point(1, 1, 1)
        result = point1 - point2

        self.assertEqual(result, 1.0)
