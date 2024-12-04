"""Basic application flow"""
import model
import view

game = model.GameModel(['Foo', 'Bar'], 6, 6)
game.create_planets(10)
print("\n".join(view.game_to_str(game)))
for turn in range(3):
    if game.is_complete():
        break
    print("taking turn")
print("game is complete")
