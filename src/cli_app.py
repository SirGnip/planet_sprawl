import model
import view


def make_game():
    if True:
        planet_in = input("Enter how many planets: ")
        planet_count = int(planet_in) if planet_in.strip() != "" else 10
        width_in = input("Enter horizontal width of map: ")
        width = int(width_in) if width_in.strip() != "" else 10
        height_in = input("Enter vertical height of map: ")
        height = int(height_in) if height_in.strip() != "" else 10
        names = []
        while True:
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
    print()
    print()
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



