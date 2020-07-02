BOARD_WIDTH = 3
BOARD_HEIGHT = 3
NUM_TO_WIN = 3
PLAYER1 = 1
PLAYER2 = 2


def player(state):
    if sum(state) % (PLAYER1 + PLAYER2) == 0:
        return PLAYER1
    else:
        return PLAYER2


def is_end(state):
    if sum(state) < PLAYER1 * NUM_TO_WIN + PLAYER2 * (NUM_TO_WIN - 1):
        return False, 0

    if player(state) == PLAYER1:
        score = 1  # PLAYER 2 wins
    else:
        score = -1  # PLAYER 1 wins
    filled = True
    for i in range(BOARD_HEIGHT * BOARD_WIDTH):
        x = i % BOARD_WIDTH
        y = i // BOARD_WIDTH
        if state[i] == 0:
            filled = False
        else:
            # In a row
            result = True
            for j in range(1, NUM_TO_WIN):
                p = x - j
                if p < 0:  # Out of board
                    result = False
                    break
                else:
                    n = p + y * BOARD_WIDTH
                    if state[n] != state[i]:
                        result = False
                        break
            if result:
                return True, score

            # In a column
            result = True
            for j in range(1, NUM_TO_WIN):
                q = y - j
                if q < 0:
                    result = False
                    break
                else:
                    m = q * BOARD_WIDTH + x
                    if state[m] != state[i]:
                        result = False
                        break
            if result:
                return True, score

            # Towards upper-left
            result = True
            for j in range(1, NUM_TO_WIN):
                p = x - j
                q = y - j
                if q < 0 or p < 0:
                    result = False
                    break
                else:
                    r = q * BOARD_WIDTH + p
                    if state[r] != state[i]:
                        result = False
                        break
            if result:
                return True, score

            # Towards upper-right
            result = True
            for j in range(1, NUM_TO_WIN):
                p = x + j
                q = y - j
                if q < 0 or p >= BOARD_WIDTH:
                    result = False
                    break
                else:
                    r = q * BOARD_WIDTH + p
                    if state[r] != state[i]:
                        result = False
                        break
            if result:
                return True, score

    if filled:
        return True, 0
    return False, 0


def actions(state):
    acts = set()
    for i in range(len(state)):
        if state[i] == 0:
            acts.add(i)
    return acts


def make_move(state, move):
    state[move] = player(state)


if __name__ == "__main__":
    game = [1, 1, 1,
            0, 2, 2,
            2, 1, 0]
    print(is_end(game))
