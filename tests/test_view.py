from model import Planet, GameModel, Grid, Point, Player, Fleet
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


def test_fleet_view():
    plyr1 = Player("FooBar")
    p1 = Planet(None, "Xylex", Point(1, 1), 0, 0)
    p2 = Planet(None, "Zeta", Point(3, 1), 0, 0)
    f1 = Fleet(plyr1, p1, p2, 2, 10)
    f2 = Fleet(plyr1, p2, p1, 3, 11)
    fleets = [f1, f2]
    txt = view.fleets_to_str(fleets)
    assert len(txt) == 2
    assert "FooB" in txt[0]
    assert "FooB" in txt[1]
    assert "X" in txt[0]
    assert "Z" in txt[1]


def test_game_view():
    """General smoke test for the GameModel view"""
    game = GameModel(["Foo", "Bar"], 6, 6)
    game.create_planets(10)
    txt = view.game_to_str(game)
    game.send(1, "A", "B", 5)
    event_lines = view.events_to_str(game.events, 1)
    assert len(event_lines) == 0
