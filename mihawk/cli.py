from pathlib import Path

from mihawk.readers import KMLReader


def main():
    """Load a KML file and find optimal path."""

    cwd = Path(__file__).parent.absolute()
    filename = cwd.joinpath("static", "agios_gewrgios.kml")

    with open(filename) as file:
        data = KMLReader(file)

    print(data.coords[0])


if __name__ == "__main__":
    main()
