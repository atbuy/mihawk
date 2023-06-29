from dataclasses import dataclass
from typing import List

from mihawk._utils import get_distance


@dataclass
class Point:
    latitude: float
    longitude: float
    elevation: float
    name: str = None

    def __eq__(self, other: "Point") -> bool:
        """Check if two points are equal."""

        return self.name == other.name

    def __sub__(self, other: "Point") -> float:
        """Calculate the euclidean distance between two points."""

        lat = (other.latitude - self.latitude) ** 2
        lon = (other.longitude - self.longitude) ** 2
        ele = (other.elevation - self.elevation) ** 2

        return (lat + lon + ele) ** 0.5

    def __hash__(self):
        """Return a hash of the UUID of the object."""

        return hash(self.name)


@dataclass
class Path:
    points: List[Point]
    length: float = None

    def __post_init__(self):
        """Calculate the length of the path."""

        self.length = self.calculate_length()

    def __iter__(self):
        """Iterate over the points in the path."""

        return iter(self.points)

    def __len__(self):
        """Return the length of the path."""

        return len(self.points)

    def calculate_length(self) -> float:
        """Calculate the length of the path."""

        length = 0
        for index in range(len(self.points) - 1):
            point = self.points[index]
            other = self.points[index + 1]
            length += get_distance(point, other)

        return length
