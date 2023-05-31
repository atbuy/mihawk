import math
from dataclasses import dataclass


@dataclass
class Point:
    latitude: float
    longitude: float
    elevation: float

    def __sub__(self, other: "Point") -> float:
        """Calculate distance between two points."""

        lat = (self.latitude - other.latitude) ** 2
        lon = (self.longitude - other.longitude) ** 2
        ele = (self.elevation - other.elevation) ** 2

        return math.sqrt(lat + lon + ele)
