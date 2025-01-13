import model
import view


def get_input(msg, default):
    val = input(msg + f"({default}) ")
    if val.strip() == "":
        val = default
    return val


def make_game():
    if True:
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
        names = ['foo', 'bar']
        width = 10
        height = 10
        planet_count = 10

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
        while True:
            turn = input("Enter moves: ")
            if turn.strip() == "":
                break
            elif turn.strip() == "q":
                break
            else:
                tokens = turn.strip().split()
                player_idx, planet_from, planet_to, ships = tokens
                player_idx = int(player_idx)
                ships = int(ships)
                game.send(player_idx, planet_from, planet_to, ships)
        game.simulate()
        if game.is_complete() or turn.strip() == "q":
            break
    game.events.add(game.turn, "GAME OVER!")
    print_game(game)


if __name__ == '__main__':
    main()



