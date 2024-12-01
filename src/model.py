import math
import random
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

    def get_all_points(self):
        return [Point(x, y) for x in range(self.width) for y in range(self.height)]


@dataclass
class Fleet:
    owner: Player
    source: Planet
    destination: Planet
    ships: int
    turn_launched: int
    _arrival_turn: int = field(init=False)

    def __post_init__(self):
        self._arrival_turn = self.turn_launched + math.ceil(self.source.pos.distance(self.destination.pos))


def name_generator(first_char):
    length = random.choice(range(3, 6))
    vowels = "aeiou"
    consonants = "bcdfghjklmnprstvwxyz"  # removed q
    name = first_char
    while len(name) < length:
        if name[-1] in vowels:
            name += random.choice(consonants)
        else:
            name += random.choice(vowels)
    return name.title()


class GameModel:
    """Top-level model that holds all individual models"""
    def __init__(self, player_names: list[str], width: int, height: int):
        self.players = [Player(name) for name in player_names]
        self.grid = Grid(width, height)
        self.fleets = []

    def create_planets(self, count):
        all_points = self.grid.get_all_points()
        random.shuffle(all_points)
        for i in range(count):
            name = name_generator(chr(ord('a') + i))
            ships = random.randint(0, 10)
            prod = random.randint(0, 10)
            owner = None
            if i < len(self.players):
                owner = self.players[i]
                ships = 50
            self.grid.add(Planet(owner, name, all_points[i], ships, prod))
