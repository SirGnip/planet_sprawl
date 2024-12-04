"""Basic application flow"""
import model
import view

game = model.GameModel(['Foo', 'Bar'], 6, 6)
game.create_planets(10)
for turn in range(3):
    print()
    print('======= Turn {} ======'.format(turn + 1))
    print("\n".join(view.game_to_str(game)))
    if game.is_complete():
        break
print("game is complete")
