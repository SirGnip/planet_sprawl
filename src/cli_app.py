import time
import asyncio
import model
import view
import player
import argparse
from player import PlayerExitException


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


def make_game(planet_count, width, height, player_configs):
    names = [conf['name'] for conf in player_configs]
    players = []
    for idx, conf in enumerate(player_configs, 1):
        ptype = conf['type'].lower()
        if ptype == 'human':
            players.append(player.ManualPlayerController(idx, conf['name']))
        elif ptype == 'ai_random':
            players.append(player.AiPlayerControllerRandom(idx, conf['name']))
        elif ptype == 'ai_spread':
            players.append(player.AiPlayerControllerSpread(idx, conf['name']))
        else:
            raise ValueError(f"Unknown player type: {conf['type']}")
    game = model.GameModel(names, width, height)
    game.create_planets(planet_count)
    return game, players


def print_game(game):
    [print() for _ in range(5)]
    print("====== Turn {} ======".format(game.turn))
    print("\n".join(view.game_to_str(game)))


def parse_cli_args_and_start_game():
    parser = argparse.ArgumentParser(description="Planet Sprawl Game")
    parser.add_argument('--planets', type=int, default=10, help='Number of planets')
    parser.add_argument('--width', type=int, default=5, help='Grid width')
    parser.add_argument('--height', type=int, default=5, help='Grid height')
    parser.add_argument('--player', action='append', nargs=2, metavar=('TYPE', 'NAME'),
                        help='Add a player: TYPE NAME (TYPE: human, ai_random, ai_spread)')
    args = parser.parse_args()

    if not args.player:
        print("At least one player required. Use --player TYPE NAME")
        exit(1)
    player_configs = [{'type': t, 'name': n} for t, n in args.player]
    game, players = run_game(args.planets, args.width, args.height, player_configs)


def main_cli():
    import sys
    if len(sys.argv) > 1:
        parse_cli_args_and_start_game()
    else:
        # Interactive fallback for manual testing
        planet_count = int(get_input("Enter how many planets: ", 10))
        width = int(get_input("Enter horizontal width of map: ", 4))
        height = int(get_input("Enter vertical height of map: ", 4))
        num_players = int(get_input("How many players? ", 2))
        player_configs = []
        for i in range(num_players):
            ptype = get_input(f"Enter player {i+1} type (human/ai_random/ai_spread): ", "human")
            name = get_input(f"Enter name for {ptype} player {i+1}: ", f"p{i+1}")
            player_configs.append({'type': ptype, 'name': name})
        run_game(planet_count, width, height, player_configs)


def run_game(planet_count, width, height, player_configs, silent=False):
    game, players = make_game(planet_count, width, height, player_configs)
    run_game_loop(game, players, silent)
    return game


async def player_main(game, players):
    tasks = [asyncio.create_task(p.make_move(game)) for p in players]
    await asyncio.gather(*tasks)  # Awaiting tasks allows exceptions to be caught and reraised by the custom event loop
    print('main is done')


def run_game_loop(game, players, silent=False):
    event_loop = PlayerEventLoop(player_main(game, players))
    while not game.is_complete():
        if not silent:
            print_game(game)
        try:
            event_loop.tick()
        except PlayerExitException as e:
            print(f"\nGame exited by player: Exception: {e}")
            break
        game.simulate()

    winner = game.get_winner()
    game.events.add(game.turn, f"GAME OVER! Winner: {winner.name}")

    if not silent:
        print_game(game)


def batch_of_games():
    cfg = [
        {'type': 'ai_random', 'name': 'rand'},
        {'type': 'ai_spread', 'name': 'alpha'},
        {'type': 'ai_spread', 'name': 'beta'},
    ]
    for i in range(10):
        game = run_game(15, 8, 8, cfg, silent=True)
        print(f'{i} {game.turn} {game.get_winner().name}')


if __name__ == '__main__':
    main_cli()
    # batch_of_games()
