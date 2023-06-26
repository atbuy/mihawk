import warnings
from abc import ABCMeta, abstractmethod
from typing import List

from matplotlib.axes import Axes

try:
    from matplotlib import pyplot as plt

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
        print("Size:", self.size)

        least_distance = float("inf")
        shortest_path = None
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
            least_distance = float("inf")
            graph[point] = []
            for other in self.points:
                if point == other:
                    continue

                distance = get_distance(point, other)
                graph[point].append(other)

                # Check if the distance is less than the current least distance
                if distance < least_distance:
                    least_distance = distance
                    point.closest = other

            # Sort each point's neighbors by distance
            graph[point].sort(key=lambda x: get_distance(point, x))

        return graph

    def solve(self, start: Point) -> Path:
        """Solve the TSP using the nearest neighbor algorithm."""

        # Loop over all points and use them as starting points
        # to find the shortest path.
        path = [start]
        while len(path) < self.size:
            current = path[-1]
            for point in self.graph[current]:
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
        end_x = len(X) - 1
        end_y = len(Y) - 1
        end_z = len(Z) - 1

        normal_x = X[1:end_x]
        normal_y = Y[1:end_y]
        normal_z = Z[1:end_z]

        ax.scatter(normal_x, normal_y, normal_z, linewidth=0.5)
        ax.scatter(X[0], Y[0], Z[0], linewidth=0.5, color="green")
        ax.scatter(X[-1], Y[-1], Z[-1], linewidth=0.5, color="red")
        ax.plot(X, Y, Z, linewidth=0.5, color="black")

        ax.view_init(20, -140)

        plt.title("Nearest Neighbor Graph")
        plt.tight_layout()
        plt.show()
