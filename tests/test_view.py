from model import Planet, Grid, Point
import view


def test_grid_view():
    g = Grid(3, 3)
    g.add(Planet(None, "Alpha", Point(0, 0), 0, 0))
    g.add(Planet(None, "Beta", Point(2, 1), 3, 1))
    g.add(Planet(None, "Cato", Point(1, 2), 5, 10))
    assert view.grid_to_str(g) == """
A..
..B
.C. 
""".strip().split("\n")
