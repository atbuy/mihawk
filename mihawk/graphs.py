import warnings

try:
    from matplotlib import pyplot as plt

    warnings.filterwarnings("ignore", module="matplotlib")
    plt.style.use("seaborn")
    VISUALIZE = True
except ImportError:
    VISUALIZE = False


class KMLGraph:
    """Represent a graph object.

    This is used after parsing a KML file and loading all the Points.
    It structures the points into a graph object, to be used by the
    dynamic programming algorithm to find the shortest path.
    """

    def __init__(self, points: list):
        self.points = points
        self.size = len(points)
        self.graph = self._structure()

    def _structure(self) -> dict:
        """Structure the points into a graph object."""

        # TODO

        graph = {}
        return graph

    def visualize(self):
        """Visualize the graph object."""

        if not VISUALIZE:
            warnings.warn("matplotlib is not installed. Skipping visualization.")
            return

        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")

        for point in self.points:
            ax.scatter(point.latitude, point.longitude, point.elevation)

        plt.tight_layout()
        plt.show()

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self):
        return f"Graph(size={self.size})"
