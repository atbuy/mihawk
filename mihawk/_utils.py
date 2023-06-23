from functools import lru_cache


@lru_cache(maxsize=None)
def get_distance(source, dest) -> float:
    """Calculate the euclidean distance between two points.

    Args:
        source (Point): The source point.
        dest (Point): The destination point.

    Returns:
        float: The euclidean distance between the two points.
    """

    return abs(source - dest)
