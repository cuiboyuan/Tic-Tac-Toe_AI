import GameRule, GameControl
q = []
q_set = set()

explored = set()

win = set()


def explore(state):
    for i in range(len(state)):
        if state[i] == 0:
            temp = list(state)
            temp[i] = GameRule.player(temp)

            board = tuple(temp)
            if board in win:
                pass
            elif GameRule.is_end(temp)[0]:
                win.add(board)
            else:
                if board not in q_set:
                    q.append(board)
                    q_set.add(board)
    explored.add(state)

if __name__ == "__main__":
    q.append((0,0,0,0,0,0,0,0,0))
    q_set.add((0,0,0,0,0,0,0,0,0))

    while q != []:
        state = q.pop(0)
        q_set.remove(state)
        explore(state)

    print(f"Total Board {len(explored)}")
    print(f"End Board {len(win)}")

