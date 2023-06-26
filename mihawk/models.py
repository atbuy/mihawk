import math
import uuid
from dataclasses import dataclass
from typing import List

from mihawk._utils import get_distance


@dataclass
class Point:
    latitude: float
    longitude: float
    elevation: float
    closest: "Point" = None

    def __post_init__(self):
        """Generate a UUID for the object."""

        self.uuid = uuid.uuid4().hex

    def __eq__(self, other: "Point") -> bool:
        """Check if two points are equal."""

        lat = self.latitude == other.latitude
        lon = self.longitude == other.longitude
        ele = self.elevation == other.elevation

        return lat and lon and ele

    def __sub__(self, other: "Point") -> float:
        """Calculate the euclidean distance between two points."""

        lat = (self.latitude - other.latitude) ** 2
        lon = (self.longitude - other.longitude) ** 2
        ele = (self.elevation - other.elevation) ** 2

        return math.sqrt(lat + lon + ele)

    def __hash__(self):
        """Return a hash of the UUID of the object."""

        return hash(self.uuid)


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
