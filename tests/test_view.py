from model import Planet, Grid, Point, Player
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


def test_planets_view():
    p1 = Player("Foo")
    p2 = Player("Buddy")
    g = Grid(3, 3)
    g.add(Planet(p1, "Alpha", Point(0, 0), 15, 1))
    g.add(Planet(p2, "Beta", Point(2, 1), 3, 2))
    g.add(Planet(None, "Cato", Point(1, 2), 7, 10))
    assert view.planets_to_str(g) == """
P Ship Prd Ownr
---------------
A   15   1 Foo
B    3   2 Budd
C    7  10 -
 """.strip().split("\n")
