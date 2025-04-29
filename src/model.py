"""
NOTE: It feels like the GameModel.parse_cli_command() method and InvalidPlayerInput
exception are pollution the encapsulation of the model by letting UI logic "leak" into it.
At least it doesn't directly depend on anything UI related.
"""


import math
import random
from dataclasses import dataclass, field


TURN = int

HOME_SHIPS = 20
HOME_PRODUCTION = 10
NEUTRAL_SHIP_MIN = 0
NEUTRAL_SHIP_MAX = 5
NEUTRAL_PRODUCTION_MIN = 0
NEUTRAL_PRODUCTION_MAX = 8
NEUTRAL_NAME = "-"


class InvalidPlayerInput(Exception):
    pass


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
    is_neutral: bool = False

    def __str__(self):
        return self.name


@dataclass
class Planet:
    owner: Player
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

    def get(self, x, y) -> Planet:
        assert 0 <= x < self.width and 0 <= y < self.height, f"Invalid coordinates: {x}, {y} outside of width & height: {self.width} {self.height}"
        planets = [p for p in self.planets if p.pos.x == x and p.pos.y == y]
        if len(planets) == 0:
            raise Exception(f"No planet at {x}, {y}")
        assert len(planets) == 1, f"Did not find one and only one planet for {x}, {y}"
        return planets[0]

    def get_planet(self, letter) -> Planet|None:
        for p in self.planets:
            if p.get_abbreviation() == letter:
                return p
        assert False, f"No planet with abbreviation: {letter}"

    def get_all_points(self):
        return [Point(x, y) for x in range(self.width) for y in range(self.height)]

    def produce(self) -> None:
        for p in self.planets:
            if not p.owner.is_neutral:
                p.ships += p.production


@dataclass
class Fleet:
    owner: Player
    source: Planet
    destination: Planet
    ships: int
    turn_launched: TURN
    _arrival_turn: TURN = field(init=False)

    def __post_init__(self):
        self._arrival_turn = self.turn_launched + math.ceil(self.source.pos.distance(self.destination.pos))


@dataclass
class EventLog:
    """List of events that happend in the game that should be displayed to the user
    Oldest event is at front of list"""
    events: list[tuple[TURN, str]] = field(default_factory=list)

    def length(self):
        return len(self.events)

    def add(self, turn: TURN, msg: str):
        self.events.append((turn, msg))


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
        self.neutral_player = Player(NEUTRAL_NAME, is_neutral=True)
        self.players.insert(0, self.neutral_player)
        self.grid = Grid(width, height)
        self.fleets = []
        self.turn = 1
        self.events = EventLog()

    def create_planets(self, count):
        all_points = self.grid.get_all_points()
        random.shuffle(all_points)
        for i in range(count):
            name = name_generator(chr(ord('a') + i))
            ships = random.randint(NEUTRAL_SHIP_MIN, NEUTRAL_SHIP_MAX)
            prod = random.randint(NEUTRAL_PRODUCTION_MIN, NEUTRAL_PRODUCTION_MAX)
            owner = self.neutral_player
            active_players = [p for p in self.players if not p.is_neutral]
            # Create starting worlds
            if i < len(active_players):
                owner = active_players[i]
                ships = HOME_SHIPS
                prod = HOME_PRODUCTION
            self.grid.add(Planet(owner, name, all_points[i], ships, prod))

    def parse_cli_command(self, player_input) -> tuple[str, str, int]:
        tokens = player_input.strip().split()
        if len(tokens) != 3:
            raise InvalidPlayerInput("Expected 3 items in input: FROM TO SHIPS")
        planet_from, planet_to, ships = tokens
        try:
            ships = int(ships)
        except Exception as exc:
            raise InvalidPlayerInput(f"Invalid ship count: {exc}")
        return planet_from.upper(), planet_to.upper(), ships

    def send(
            self,
            player_idx: int,
            from_planet: str,
            to_planet: str,
            ships: int) -> None:
        assert player_idx < len(self.players), f"Invalid player index: {player_idx}"
        src = self.grid.get_planet(from_planet)
        trg = self.grid.get_planet(to_planet)

        player = self.players[player_idx]
        assert player == src.owner, f"{player.name} does not own {src.get_abbreviation()}"
        assert ships <= src.ships, f"{player.name} does not have {ships} ships on {src.get_abbreviation()}. There are {src.ships}."
        fleet = Fleet(player, src, trg, ships, self.turn)
        src.ships -= fleet.ships
        print('SEND', fleet)
        self._add_fleet(fleet)

    def _add_fleet(self, fleet: Fleet):
        self.fleets.append(fleet)

    def is_complete(self):
        players = {p.owner for p in self.grid.planets if not p.owner.is_neutral}
        if len(players) > 1:
            return False
        last_player = players.pop()
        print(f'complete: {last_player}')
        for f in self.fleets:
            print(f'  fleet: {f}')
        return all(fleet.owner == last_player for fleet in self.fleets)

    def add_event(self, msg: str):
        self.events.add(self.turn, msg)

    def simulate(self):
        """Move fleets, resolve conflicts, handle planet production"""
        # TEMP impl, just gets the tests to pass
        self.turn += 1

        # production
        self.grid.produce()

        # fleets
        new_fleets = []
        for fleet in self.fleets:
            if fleet._arrival_turn <= self.turn:
                trg = fleet.destination
                if fleet.owner == trg.owner:
                    self.add_event(f"{fleet.owner.name} REINFORCED {trg.get_abbreviation()} with {fleet.ships} ships")
                    trg.ships += fleet.ships
                else:
                    if fleet.ships > trg.ships:
                        self.add_event(f"{fleet.owner.name} CONQUERED {trg.owner.name} on {trg.get_abbreviation()} using {fleet.ships} ships")
                        trg.owner = fleet.owner
                        trg.ships = fleet.ships - trg.ships
                    else:
                        self.add_event(f"{trg.owner.name} DEFENDED {fleet.owner.name}'s {fleet.ships} ship attack on {trg.get_abbreviation()}")
                        trg.ships -= fleet.ships
            else:
                new_fleets.append(fleet)

        self.fleets = new_fleets
