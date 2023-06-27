import warnings
from abc import ABCMeta, abstractmethod
from typing import List

import numpy as np

try:
    from matplotlib import pyplot as plt
    from matplotlib.axes import Axes

    warnings.filterwarnings("ignore", module="matplotlib")
    plt.style.use("seaborn")
    VISUALIZE = True
except ImportError:
    VISUALIZE = False

from mihawk._utils import get_distance
from mihawk.models import Path, Point


class KMLGraph(metaclass=ABCMeta):
    """Represent a graph object.

    This is used after parsing a KML file and loading all the Points.
    It structures the points into a graph object, to be used by the
    dynamic programming algorithm to find the shortest path.
    """

    def __init__(self, points: List[Point]):
        self.points = points
        self.size = len(points)

    @abstractmethod
    def _build_graph(self) -> dict:
        """Build the graph object."""

        raise NotImplementedError

    @abstractmethod
    def solve(self, start: Point) -> Path:
        """Solve the TSP using the nearest neighbor algorithm."""

        raise NotImplementedError

    @abstractmethod
    def visualize(self):
        """Visualize the graph object."""

        raise NotImplementedError

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(size={self.size})"


class NearestNeighborGraph(KMLGraph):
    """Represent a graph object using the nearest neighbor algorithm."""

    def __init__(self, points: List[Point]):
        super().__init__(points)
        self.graph = self._build_graph()

        least_distance = float("inf")
        shortest_path = None
        self.points = np.array(self.points)
        for point in self.points:
            path = self.solve(point)
            if path.length < least_distance:
                shortest_path = path
                least_distance = path.length

        self.path = shortest_path

    def _build_graph(self) -> dict:
        """Build the graph object."""

        # Iterate over all the points
        # and each point's closest neighbor.
        graph = {}
        for point in self.points:
            graph[point] = self.points.copy()
            graph[point].remove(point)
            graph[point].sort(key=lambda x: get_distance(point, x))

        return graph

    def solve(self, start: Point) -> Path:
        """Solve the TSP using the nearest neighbor algorithm."""

        # Loop over all points and use them as starting points
        # to find the shortest path.
        path = [start]
        current = start
        while len(path) < self.size:
            current = path[-1]
            neighbors = self.graph[current]
            for point in neighbors:
                if point not in path:
                    path.append(point)
                    break

        return Path(path)

    def visualize(self):
        """Visualize the graph object."""

        if not VISUALIZE:
            warnings.warn("matplotlib is not installed. Skipping visualization.")
            return

        fig = plt.figure()
        ax: Axes = fig.add_subplot(projection="3d")

        # Set the X, Y, Z coordinates
        X = [point.latitude for point in self.path]
        Y = [point.longitude for point in self.path]
        Z = [point.elevation for point in self.path]

        # Plot the points and connect them
        normal_x = X[1 : len(X) - 1]
        normal_y = Y[1 : len(Y) - 1]
        normal_z = Z[1 : len(Z) - 1]

        ax.scatter(X[0], Y[0], Z[0], color="red")
        ax.scatter(X[-1], Y[-1], Z[-1], color="red")
        ax.scatter(normal_x, normal_y, normal_z, linewidth=0.5)
        ax.plot(X, Y, Z, linewidth=0.5)

        ax.view_init(30, -115)

        plt.title("Nearest Neighbor Graph")
        plt.tight_layout()
        plt.show()


class MultiGraph:
    """Used to visualize multiple graphs at once."""

    def __init__(self, multi_data: List[List[Point]], filenames: List[str]):
        self.multi = multi_data
        self.graphs = [NearestNeighborGraph(data) for data in self.multi]
        self.filenames = filenames

    def visualize(self):
        """Visualize all graphs in subplots"""

        if not VISUALIZE:
            warnings.warn("matplotlib is not installed. Skipping visualization.")
            return

        fig = plt.figure()
        max_col = 5
        leftover = len(self.graphs) % max_col
        rows = (len(self.graphs) // max_col) + leftover
        for i, graph in enumerate(self.graphs):
            # Set the X, Y, Z coordinates
            X = [point.latitude for point in graph.path]
            Y = [point.longitude for point in graph.path]
            Z = [point.elevation for point in graph.path]

            # Plot the points and connect them
            normal_x = X[1 : len(X) - 1]
            normal_y = Y[1 : len(Y) - 1]
            normal_z = Z[1 : len(Z) - 1]

            ax = fig.add_subplot(rows, max_col, i + 1, projection="3d")
            ax.scatter(X[0], Y[0], Z[0], color="red")
            ax.scatter(X[-1], Y[-1], Z[-1], color="red")
            ax.scatter(normal_x, normal_y, normal_z, linewidth=0.5)
            ax.plot(X, Y, Z, linewidth=0.5)

            ax.set_title(self.filenames[i])
            ax.view_init(30, -115)

        plt.title("Nearest Neighbor Graph")
        plt.tight_layout()
        plt.show()
