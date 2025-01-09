"""Test basic application flow as a smoke test of sorts"""
import model
import view


def _create_test_game() -> model.GameModel:
    game = model.GameModel(["Foo", "Bar"], 4, 4)
    game.grid.add(model.Planet(game.players[0], 'Able', model.Point(0, 0), 20, 1))
    game.grid.add(model.Planet(game.players[1], 'Beta', model.Point(3, 0), 10, 1))
    return game


def print_game(game):
    print()
    print("====== Turn {} ======".format(game.turn))
    print("\n".join(view.game_to_str(game)))


def game_loop(turn_fn):
    game = _create_test_game()
    while not game.is_complete():
        print_game(game)
        turn_fn(game)
        game.simulate()
        if game.is_complete():
            break
        if game.turn > 10:
            break
    game.events.add(game.turn, "GAME OVER!")
    print_game(game)


def turn_sim1(game):
    if game.turn == 1:
        game.send(0, "A", "B", 3)
    elif game.turn == 3:
        game.send(0, "A", "B", 15)


def turn_sim2(game):
    if game.turn == 1:
        game.send(1, "B", "A", 10)
    elif game.turn == 3:
        game.send(0, "A", "B", 20)


def test_game1():
    game_loop(turn_sim1)


def test_game2():
    game_loop(turn_sim2)
