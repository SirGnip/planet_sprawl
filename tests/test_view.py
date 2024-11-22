from model import Planet, Grid, Point
import view


def test_grid_view():
    g = Grid(3, 3)
    g.add(Planet(None, "Alpha", Point(0, 0), 0, 0))
    g.add(Planet(None, "Beta", Point(2, 1), 3, 1))
    assert view.grid_to_str(g) == """
. . .
. . B
A . . 
""".strip().split("\n")
