import random
import asyncio
import model

class PlayerExitException(Exception):
    """Raised when a manual player exits the game interactively."""
    # BUG: The custom async loop is somehow delaying the catching of exceptions. So, a game exit is delayed a couple turns.
    pass

class PlayerController:
    def __init__(self, idx: int, name: str):
        self.idx = idx
        self.name = name

    def get_name(self):
        return self.name

    async def make_move(self, game: model.GameModel):
        pass

class ManualPlayerController(PlayerController):
    def __init__(self, idx: int, name: str):
        super().__init__(idx, name)

    async def make_move(self, game: model.GameModel):
        while True:  # Loop for entire game
            while True:  # Loop to get multiple moves
                turn = input(f"  Enter move for {self.get_name()} #{self.idx} (<FROM> <TO> <SHIPS>, empty to end turn, or 'quit' to quit game completely): ")
                if turn.strip().lower() == 'quit':
                    print(f"Player {self.get_name()} ({self.idx}) exited the game.")
                    raise PlayerExitException(f"Player {self.get_name()} exited the game.")
                if turn.strip() == "":
                    break  # done entering moves for this turn
                try:
                    planet_from, planet_to, ships = game.parse_cli_command(turn)
                    game.send(self.idx, planet_from, planet_to, ships)
                except Exception as exc:
                    print(f"  Invalid input: {exc.__class__.__name__}: {exc}")
            await asyncio.sleep(0)

class AiPlayerController(PlayerController):
    def __init__(self, idx: int, name: str):
        super().__init__(idx, name)

class AiPlayerControllerMinimal(AiPlayerController):
    """A minimal player. Not very useful."""
    async def make_move(self, game: model.GameModel):
        game.send(self.idx, "A", "C", 10)
        await asyncio.sleep(0)
        while True:
            game.send(self.idx, "A", "C", 5)
            await asyncio.sleep(0)

class AiPlayerControllerRandom(AiPlayerController):
    """Randomly select 'from' and 'to' planets. This simple logic can 'win'."""
    async def make_move(self, game: model.GameModel):
        while True:
            my_planets = [p for p in game.grid.planets if p.owner.name == self.get_name()]
            non_owned_planets = [p for p in game.grid.planets if p.owner.name != self.get_name()]
            if len(my_planets) > 0 and len(non_owned_planets) > 0:
                from_planet = random.choice(my_planets)
                to_planet = random.choice(non_owned_planets)
                ships = int(from_planet.ships * 0.75)
                if ships > 0:
                    game.send(self.idx, from_planet.get_abbreviation(), to_planet.get_abbreviation(), ships)
            await asyncio.sleep(0)

class AiPlayerControllerSpread(AiPlayerController):
    """Attack planet nearest to the planets I own."""
    async def make_move(self, game: model.GameModel):
        while True:
            # attack
            my_planets = [p for p in game.grid.planets if p.owner.name == self.get_name()]
            enemy_planets = [p for p in game.grid.planets if p.owner.name != self.get_name()]
            if len(my_planets) > 0 and len(enemy_planets) > 0:
                closest_enemy = min(enemy_planets, key=lambda e: min(e.pos.distance(p.pos) for p in my_planets))
                closest_my_planet = min(my_planets, key=lambda p: closest_enemy.pos.distance(p.pos))
                ships = int(closest_my_planet.ships * 0.8)
                if ships > 0:
                    # print(f"*** {self.name} Attack-Sending {ships} ships from {closest_my_planet.get_abbreviation()} to {closest_enemy.get_abbreviation()}")
                    game.send(self.idx, closest_my_planet.get_abbreviation(), closest_enemy.get_abbreviation(), ships)

                # fortify - from planet with most ships to planet that is attacking
                most_ships_planet = max(my_planets, key=lambda p: p.ships)
                ships = int(most_ships_planet.ships * 0.8)
                if most_ships_planet.ships > 10:
                    # print(f"*** {self.name} Fortify-Sending {ships} ships from {most_ships_planet.get_abbreviation()} to {closest_my_planet.get_abbreviation()}")
                    game.send(self.idx, most_ships_planet.get_abbreviation(), closest_my_planet.get_abbreviation(), ships)

            await asyncio.sleep(0)
