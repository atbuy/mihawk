import time
from pathlib import Path

from mihawk.graphs import NearestNeighborGraph
from mihawk.readers import KMLReader


def main():
    """Load a KML file and find optimal path."""

    cwd = Path(__file__).parent.absolute()
    filename = cwd.joinpath("static", "agios_gewrgios.kml")

    with open(filename) as file:
        data = KMLReader(file)

    # Structure points into a graph
    start = time.perf_counter()
    graph = NearestNeighborGraph(data.points)
    delta = time.perf_counter() - start

    # print(f"Path: {graph.path}")
    print(f"Graph: {graph}")
    print(f"Time: {delta:.5f}s")

    graph.visualize()


if __name__ == "__main__":
    main()
