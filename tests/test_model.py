import pytest

from model import Point, Player, Planet, GameModel, Grid, Fleet


def test_point():
    p = Point(1, 2)
    q = Point(3, 4)
    assert p != q
    assert p.distance(q) == pytest.approx(2.82842712)


def test_player():
    p = Player("Bar")
    assert p.name == "Bar"


def test_planet():
    plyr1 = Player("Foo")

    p1 = Planet(None, "Altair", Point(5, 5), 5, 2)
    assert p1.owner is None
    assert p1.name == "Altair"
    assert p1.get_abbreviation() == "A"
    assert p1.pos == Point(5, 5)
    assert p1.ships == 5
    assert p1.production == 2

    p2 = Planet(plyr1, "Beta", Point(3, 7), 3, 10)
    assert p2.owner == plyr1


def test_grid():
    g = Grid(4, 5)
    assert g.width == 4
    assert g.height == 5
    assert g.planets == []

    planet1 = Planet(None, "Altair", Point(1, 1), 5, 2)
    g.add(planet1)
    planet2 = Planet(None, "Beta", Point(2, 2), 10, 5)
    g.add(planet2)
    assert len(g.planets) == 2
    assert g.planets[0] == planet1
    assert g.planets[1] == planet2
    assert g.is_complete()
    assert g.get(2, 2) == planet2
    with pytest.raises(Exception):
        g.get(0, 0)


def test_fleet():
    plyr1 = Player("Foo")
    p1 = Planet(None, "Altair", Point(1, 1), 0, 0)
    p2 = Planet(None, "Beta", Point(3, 1), 0, 0)
    f = Fleet(plyr1, p1, p2, 5, 10)
    assert f.owner == plyr1
    assert f.source == p1
    assert f.destination == p2
    assert f.ships == 5
    assert f.turn_launched == 10
    assert f._arrival_turn == 12


def _create_test_game() -> GameModel:
    game = GameModel(["Foo", "Bar"], 4, 4)
    game.grid.add(Planet(game.players[0], 'Able', Point(0, 0), 10, 1))
    game.grid.add(Planet(game.players[1], 'Beta', Point(3, 0), 10, 1))
    return game


def test_game():
    """Basic smoke test for the sequence of a full game"""
    game = _create_test_game()
    assert not game.is_complete()
    assert game.turn == 1
    f = Fleet(game.players[0], game.grid.get_planet("A"), game.grid.get_planet("B"), 5, game.turn)
    game.add_fleet(f)
    game.simulate()
    assert game.turn == 2
    assert not game.is_complete()
