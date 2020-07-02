from GameAI import GameAI
import GameRule

import json

BRAINS_PATH = "brains/"

board = []
for _ in range(GameRule.BOARD_HEIGHT * GameRule.BOARD_WIDTH):
    board.append(0)
history = []

AIs = {}


def player_make_move(move):
    if not is_end():
        history.append(move)
        GameRule.make_move(board, move)


def print_game():
    display = ""
    for i in range(GameRule.BOARD_HEIGHT):
        display += "|"
        for j in range(GameRule.BOARD_WIDTH):
            holder = board[i * GameRule.BOARD_WIDTH + j]
            if holder == GameRule.PLAYER1:
                display += "X "
            elif holder == GameRule.PLAYER2:
                display += "O "
            else:
                display += "{} ".format(i * GameRule.BOARD_WIDTH + j)
        display = display.strip()
        display += "|\n"
    print(display)


def restart():
    for i in range(GameRule.BOARD_HEIGHT * GameRule.BOARD_WIDTH):
        board[i] = 0
    history.clear()


def whos_turn():
    return GameRule.player(board)


def available_action():
    return GameRule.actions(board)


def is_end():
    return GameRule.is_end(board)[0]


def winner():
    if is_end():
        victor = GameRule.is_end(board)[1]
        if victor == -1:
            return GameRule.PLAYER1
        elif victor == 1:
            return GameRule.PLAYER2
        else:
            return 0


def load_new_AI(file_name):
    if file_name not in AIs:
        with open(BRAINS_PATH+file_name, "r") as file:
            brain = json.load(file)
            AI = GameAI(brain)
            AIs[file_name] = AI
    else:
        print("AI already loaded")


def ai_make_move(name, rand=False):


    move = AIs[name].pick_move(board, rand=rand)
    player_make_move(move)
    print(f"{name} made move [{move}]")


def ais_remember_game():
    if is_end():
        for name in AIs:
            AI = AIs[name]
            AI.q_eval_finished(board, history)

            with open(BRAINS_PATH+name, "w") as file:
                json.dump(AI.memory, file)
            print(f"Game saved for {name}")


def reset_AIs():
    AIs.clear()
