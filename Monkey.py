import random
import GameControl

def take_move():
    move = random.choice(list(GameControl.available_action()))
    GameControl.player_make_move(move)
