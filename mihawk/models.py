import math
import uuid
from dataclasses import dataclass


@dataclass
class Point:
    latitude: float
    longitude: float
    elevation: float

    def __post_init__(self):
        """Generate a UUID for the object."""

        self.uuid = uuid.uuid4().hex

    def __sub__(self, other: "Point") -> float:
        """Calculate the euclidean distance between two points."""

        lat = (self.latitude - other.latitude) ** 2
        lon = (self.longitude - other.longitude) ** 2
        ele = (self.elevation - other.elevation) ** 2

        return math.sqrt(lat + lon + ele)

    def __hash__(self):
        """Return a hash of the UUID of the object."""

        return hash(self.uuid)
