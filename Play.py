import GameRule, GameControl


if __name__ == "__main__":
    invalid = True
    while invalid:
        ai = input("Load AI: ")
        try:
            GameControl.load_new_AI(ai)
        except FileNotFoundError:
            invalid = True
            print("Invalid")
            continue

        print(f"AI {ai} loaded.")
        invalid = False

    while input("Enter to restart:") != "x":

        invalid = True
        while invalid:
            first = input("Go first?(y/n): ")
            if first not in ["y", "n"]:
                invalid = True
                print("Invalid")
                continue
            invalid = False
        if first == 'y':
            first = True
        else:
            first = False

        GameControl.restart()
        finish = False
        GameControl.print_game()

        while not finish:
            if first:
                turn = GameRule.PLAYER2
            else:
                turn = GameRule.PLAYER1

            if GameControl.whos_turn() == turn:
                GameControl.ai_make_move(ai)
            else:
                invalid = True
                while invalid:
                    choice = input("player move: ")
                    try:
                        move = int(choice)
                    except ValueError:
                        invalid = True
                        print("Invalid")
                        continue
                    if move not in GameControl.available_action():
                        invalid = True
                        print("Invalid")
                        continue
                    invalid = False
                    GameControl.player_make_move(int(choice))

            GameControl.print_game()

            finish = GameControl.is_end()

        if GameControl.winner() == GameRule.PLAYER1 and not first or (
                GameControl.winner() == GameRule.PLAYER2 and first):
            print("**AI wins**")
        elif GameControl.winner() == GameRule.PLAYER2 and not first or (
                GameControl.winner() == GameRule.PLAYER1 and first):
            print("**Player wins**")
        else:
            print("**Draw**")

        GameControl.ais_remember_game()
