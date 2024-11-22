import pytest

from model import Point, Player, Planet


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
