import time
import asyncio
import model
import view
import player

DEBUG = True


class PlayerEventLoop:
    def __init__(self, main_coro):
        self.loop = asyncio.get_event_loop()
        self.task = self.loop.create_task(main_coro)
        self.is_done = False

    def tick(self):
        if self.task.done():
            if not self.is_done:
                self.is_done = True
                self.loop.close()
                exc = self.task.exception()
                if exc is not None:
                    raise exc
        else:
            self.loop.call_soon(self.loop.stop)
            self.loop.run_forever()

        time.sleep(0.01)



def get_input(msg, default):
    val = input(msg + f"({default}) ")
    if val.strip() == "":
        val = default
    return val


def make_game():
    if not DEBUG:
        planet_count = get_input("Enter how many planets: ", 10)
        width = get_input("Enter horizontal width of map: ", 4)
        height = get_input("Enter vertical height of map: ", 4)
        default_names = ["foo", "buzz"]
        names = []
        while True:
            if len(default_names) > 0:
                name = get_input("Enter name: ", default_names.pop(0))
            else:
                name = input("Enter name (empty to end): ")
            if name.strip() == "":
                break
            names.append(name)
        players = []  # HACK
    else:
        players = [
            # player.ManualPlayerController(1, "Humn"),
            player.AiPlayerControllerRandom(1, "Alph"),
            player.AiPlayerControllerRandom(2, "Beta"),
            player.AiPlayerControllerRandom(3, "Cato"),
            player.AiPlayerControllerRandom(4, "Dogo"),
        ]
        names = [p.get_name() for p in players]
        planet_count = 10
        width = 5
        height = 5

    game = model.GameModel(names, width, height)
    game.create_planets(planet_count)
    return game, players


def print_game(game):
    [print() for _ in range(5)]
    print("====== Turn {} ======".format(game.turn))
    print("\n".join(view.game_to_str(game)))


async def player_main(game, players):
    tasks = [asyncio.create_task(p.make_move(game)) for p in players]
    print(f'got {len(tasks)} tasks')
    await asyncio.gather(*tasks)  # Awaiting tasks allows exceptions to be caught and reraised by the custom event loop
    print('main is done')


def run_game_loop(game, players):
    event_loop = PlayerEventLoop(player_main(game, players))
    while not game.is_complete():
        print_game(game)
        event_loop.tick()
        game.simulate()
    game.events.add(game.turn, "GAME OVER!")
    print_game(game)


def main():
    game, players = make_game()
    run_game_loop(game, players)


if __name__ == '__main__':
    main()
