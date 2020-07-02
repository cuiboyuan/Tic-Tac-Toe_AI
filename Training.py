import GameControl, GameRule

if __name__ == "__main__":

    # Load 2 AIs
    ai_x, ai_o = "", ""
    invalid = True
    while invalid:
        ai_x = input("Load first AI('X'): ")
        try:
            GameControl.load_new_AI(ai_x)
        except FileNotFoundError:
            invalid = True
            print("Invalid")
            continue

        print(f"AI {ai_x} loaded.")
        invalid = False

    invalid = True
    while invalid:
        ai_o = input("Load second AI('O'): ")
        try:
            GameControl.load_new_AI(ai_o)
        except FileNotFoundError:
            invalid = True
            print("Invalid")
            continue

        print(f"AI {ai_o} loaded.")
        invalid = False

    while True:
        num = 0
        # Load training number
        invalid = True
        while invalid:
            num = input("Number of Training:")
            try:
                num = int(num)
            except ValueError:
                invalid = True
                print("Invalid")
                continue
            if num < 0:
                invalid = True
                print("Invalid")
                continue
            invalid = False

        # For statistics
        all_history = set()
        x = 0
        o = 0
        d = 0

        # Training starts
        for i in range(num):
            print(f"Training({i + 1}/{num}):")
            GameControl.restart()
            finish = False
            # GameControl.print_game()

            # Individual Game
            # first = False
            while not finish:
                # if first:
                #     turn = GameRule.PLAYER2
                # else:
                #     turn = GameRule.PLAYER1

                if GameControl.whos_turn() == GameRule.PLAYER1:
                    GameControl.ai_make_move(ai_x, rand=True)

                else:
                    GameControl.ai_make_move(ai_o, rand=True)

                GameControl.print_game()

                finish = GameControl.is_end()

            # Switch X and O
            # first = not first

            # For statistics
            all_history.add(tuple(GameControl.history))

            # Determine winner
            if GameControl.winner() == GameRule.PLAYER1:
                print(f"**AI {ai_x}('X') wins**")
                x += 1
            elif GameControl.winner() == GameRule.PLAYER2:
                print(f"**AI {ai_o}('O') wins**")
                o += 1
            else:
                print("**Draw**")
                d += 1

            # IMPORTANT: AI learns from this game
            GameControl.ais_remember_game()

        print()
        print(f"X wins: {x}")
        print(f"O wins: {o}")
        print(f"Draw: {d}")
        print(f"{len(all_history)} different games out of {num}\n")
