import random
import GameControl

POSSIBLE_WINS = (0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (
    2, 5, 8), (0, 4, 8), (2, 4, 6)
PLAYER_FIRST = False


def take_move(player_first=True):
    move = take_turn_ai(GameControl.board, player_first=player_first)
    GameControl.player_make_move(move)


# Functions for AI:


def actions(state):
    acts = set()
    for i in range(len(state)):
        pcs = state[i]
        if pcs == 0:
            acts.add(i)
    return acts


def base_eval(state):
    for case in POSSIBLE_WINS:
        if state[case[0]] == state[case[1]] and state[case[1]] == state[
            case[2]]:
            if state[case[0]] == 0 or state[case[1]] == 0 or state[
                case[2]] == 0:
                continue
            else:
                if state[case[0]] == 2:
                    return 1
                else:
                    return -1
    return 0


def max_eval(state):
    if is_end(state):
        return base_eval(state)
    else:
        optimal = 2
        for act in actions(state):
            next_state = result(state, act)

            optimal = min(optimal, min_eval(next_state))
            if optimal == -1:
                break

        return optimal


def min_eval(state):
    if is_end(state):
        return base_eval(state)
    else:
        minimal = -2
        for act in actions(state):
            next_state = result(state, act)

            minimal = max(minimal, max_eval(next_state))
            if minimal == 1:
                break
        return minimal


def take_turn_ai(state, player_first=True):
    if sum(state) == 0:
        move = random.choice(range(0, 9))
        return move
    else:
        if player_first:
            temp = -2
        else:
            temp = 2
        move = -1
        for act in actions(state):
            pseudo_rand = random.choice([True, False])
            if player_first:
                score = max_eval(result(state, act))
                if score > temp:
                    temp = score
                    move = act
            else:
                score = min_eval(result(state, act))
                if score < temp:
                    temp = score
                    move = act

            if pseudo_rand:
                if score == temp:
                    temp = score
                    move = act

        return move


# Code for Game Basics:

def is_end(state):
    if sum(state) == 13:
        return True
    for case in POSSIBLE_WINS:
        if state[case[0]] == state[case[1]] and state[case[1]] == state[
            case[2]]:
            if state[case[0]] == 0 or state[case[1]] == 0 or state[
                case[2]] == 0:
                continue
            else:
                return True
    return False


def player(state):
    if sum(state) % 3 == 0:
        return 1
    else:
        return 2


def result(state, move):
    ret = state.copy()
    if ret[move] == 0:
        ret[move] = player(ret)
        return ret
    else:
        return None
