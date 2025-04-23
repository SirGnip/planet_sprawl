import model
import view

DEBUG = True


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
    else:
        names = ["foo", "buzz"]
        planet_count = 10
        width = 4
        height = 4

    game = model.GameModel(names, width, height)
    game.create_planets(planet_count)
    return game


def print_game(game):
    [print() for _ in range(5)]
    print("====== Turn {} ======".format(game.turn))
    print("\n".join(view.game_to_str(game)))


def main():
    game = make_game()
    while not game.is_complete():
        print_game(game)
        for player_idx, player in enumerate(game.players):
            if player.is_neutral:
                continue
            print(f"Player {player_idx} ({player.name})'s turn:")
            while True:
                turn = input(f"  Enter move for {player.name} (FROM TO SHIPS or empty to end, q to quit): ")
                if turn.strip() == "":
                    break
                if turn.strip() == "q":
                    game.events.add(game.turn, "GAME OVER!")
                    print_game(game)
                    return
                try:
                    planet_from, planet_to, ships = game.parse_cli_command(turn)
                    game.send(player_idx, planet_from, planet_to, ships)
                except Exception as exc:
                    print(f"  Invalid input: {exc.__class__.__name__}: {exc}")
        game.simulate()
    game.events.add(game.turn, "GAME OVER!")
    print_game(game)


if __name__ == '__main__':
    main()
