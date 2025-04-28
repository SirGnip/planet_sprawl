import random
import asyncio
import model


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
                turn = input(f"  Enter move for {self.get_name()} {self.idx} (<FROM> <TO> <SHIPS> or empty to end): ")
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


class AiPlayerControllerMinimal(PlayerController):
    """A minimal player. Not very useful."""
    async def make_move(self, game: model.GameModel):
        game.send(self.idx, "A", "C", 10)
        await asyncio.sleep(0)
        while True:
            game.send(self.idx, "A", "C", 5)
            await asyncio.sleep(0)


class AiPlayerControllerRandom(PlayerController):
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
