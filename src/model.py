import math
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def distance(self, other: 'Point') -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"


@dataclass(frozen=True)
class Player:
    name: str


@dataclass
class Planet:
    owner: Player | None
    name: str
    pos: Point
    ships: int
    production: int

    def get_abbreviation(self):
        return self.name[0].upper()


@dataclass
class Grid:
    """Origin is at top-left"""
    width: int
    height: int
    planets: list[Planet] = field(default_factory=list)

    def add(self, planet: Planet):
        self.planets.append(planet)

@dataclass
class Fleet:
    owner: Player
    source: Planet
    destination: Planet
    turn_launched: int
    _arrival_turn: int = field(init=False)

    def __post_init__(self):
        self._arrival_turn = self.turn_launched + math.ceil(self.source.pos.distance(self.destination.pos))