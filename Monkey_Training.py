import GameControl, GameRule, Master, Monkey
import time

if __name__ == "__main__":

    # Load 2 AIs
    ai_x = ""
    invalid = True
    while invalid:
        ai_x = input("Load student AI: ")
        try:
            GameControl.load_new_AI(ai_x)
        except FileNotFoundError:
            invalid = True
            print("Invalid")
            continue

        print(f"AI {ai_x} loaded.")
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
        m = 0
        n = 0
        d = 0

        first = True

        begin = time.time()

        # Training starts
        for i in range(num):
            print(f"Training({i + 1}/{num}):")
            GameControl.restart()
            finish = False

            if first:
                turn = GameRule.PLAYER1
            else:
                turn = GameRule.PLAYER2

            # Individual Game
            while not finish:

                if GameControl.whos_turn() == turn:
                    Monkey.take_move()

                else:
                    Master.take_move(player_first=first)

                GameControl.print_game()

                finish = GameControl.is_end()

            # For statistics
            all_history.add(tuple(GameControl.history))

            # Determine winner
            if GameControl.winner() == GameRule.PLAYER1 and not first or (
                    GameControl.winner() == GameRule.PLAYER2 and first):
                print("**Master wins**")
                m += 1
            elif GameControl.winner() == GameRule.PLAYER2 and not first or (
                    GameControl.winner() == GameRule.PLAYER1 and first):
                print("**Monkey wins**")
                n += 1
            else:
                print("**Draw**")
                d += 1

            # IMPORTANT: AI learns from this game
            GameControl.ais_remember_game()

            # Switch X and O
            first = not first

        print()
        print(f"Master wins: {m}")
        print(f"Monkey wins: {n}")
        print(f"Draw: {d}")
        print(f"{len(all_history)} different games out of {num}\n")

        print(f"Total State in Memory: {len(GameControl.AIs[ai_x].memory)}\n")
        print(f"Time:{(time.time()-begin)/60} mins")
