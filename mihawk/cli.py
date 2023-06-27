import time
from pathlib import Path

from mihawk.graphs import MultiGraph, NearestNeighborGraph
from mihawk.readers import KMLReader


def multigraph():
    """Load all KML files and find optimal path."""

    cwd = Path(__file__).parent.absolute()
    directory = cwd.joinpath("static")
    files = directory.glob("*.kml")
    multi_data = []
    filenames = []
    for file in files:
        filenames.append(file.name)
        with open(file) as f:
            data = KMLReader(f)
        multi_data.append(data.points)

        # Structure points into a graph
    start = time.perf_counter()
    multi_graph = MultiGraph(multi_data, filenames=filenames)
    delta = time.perf_counter() - start

    print(f"Time: {delta:.5f}s")

    multi_graph.visualize()


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

    print(f"Graph: {graph}")
    print(f"Time: {delta:.5f}s")

    graph.visualize()


if __name__ == "__main__":
    main()
