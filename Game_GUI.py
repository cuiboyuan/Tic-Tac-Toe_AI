from tkinter import Tk, messagebox, Button, Canvas, PhotoImage
import GameRule, GameControl

BOARD_WIDTH = 535
BOARD_HEIGHT = 536

X_RATE = 180
Y_RATE = 180

X_OFFSET = 80
Y_OFFSET = 80

# AI that is the opponent
AI_NAME = "MKY2.json"

root = Tk()
root.resizable(width=False, height=False)
root.title("Tic-Tac-Toe AI")

canvas = Canvas(root, width=BOARD_WIDTH, height=BOARD_HEIGHT)
canvas.pack()

# Store all Xs and Os image on the canvas, in case of memory leak
all_images = {}

# Whether player goes first
first = True

"""Start and Restart the game"""


def start():
    GameControl.restart()
    update_board()
    all_images.clear()

    global first

    first = messagebox.askyesno("Player first?", "Go first?")

    print("--New Game--")

    GameControl.load_new_AI(AI_NAME)

    if not first:
        GameControl.ai_make_move(AI_NAME)
        update_board()


# Config the restart button
restart = Button(root, text="Restart", command=start)
restart.pack()

# Prepare the images
board = PhotoImage(file="images/ttt.png")
O = PhotoImage(file="images/O.png")
X = PhotoImage(file="images/X.png")
select = PhotoImage(file="images/selected.png")

# Initialize the canvas
canvas.create_image(BOARD_HEIGHT / 2, BOARD_WIDTH / 2, image=board)
selected = canvas.create_image(-100, -100, image=select)

"""Update the canvas based on the board inside GameControl"""


def update_board():
    for i in range(len(GameControl.board)):
        holder = GameControl.board[i]
        if holder == GameRule.PLAYER1:
            # The actual coordinate on canvas
            coord_x = i % GameRule.BOARD_HEIGHT * X_RATE + X_OFFSET
            coord_y = i // GameRule.BOARD_HEIGHT * Y_RATE + Y_OFFSET

            # Keep track of all X and O images
            if i not in all_images:
                all_images[i] = canvas.create_image(coord_x, coord_y, image=X)

        elif holder == GameRule.PLAYER2:
            coord_x = i % GameRule.BOARD_HEIGHT * X_RATE + X_OFFSET
            coord_y = i // GameRule.BOARD_HEIGHT * Y_RATE + Y_OFFSET

            # Keep track of all X and O images
            if i not in all_images:
                all_images[i] = canvas.create_image(coord_x, coord_y, image=O)

        else:
            # Remove image form canvas if that on GameControl.board is removed
            if i in all_images:
                canvas.delete(all_images[i])

    if GameControl.is_end():

        if GameControl.winner() == GameRule.PLAYER1 and not first or (
                GameControl.winner() == GameRule.PLAYER2 and first):
            result = "**AI wins**"
        elif GameControl.winner() == GameRule.PLAYER2 and not first or (
                GameControl.winner() == GameRule.PLAYER1 and first):
            result = "**Player wins**"
        else:
            result = "**Draw**"

        GameControl.ais_remember_game()

        messagebox.showinfo("Result", result)

        if messagebox.askyesno("Restart?", "Go again?"):
            start()


"""Update the canvas with X and O images when clicked"""


def click_handler(event):
    if GameControl.is_end():
        pass
    else:
        # Find the index on GameControl.board
        selected_x = (event.x // X_RATE) * X_RATE + X_OFFSET
        selected_y = (event.y // Y_RATE) * Y_RATE + Y_OFFSET

        i = (selected_x - X_OFFSET) // X_RATE
        j = (selected_y - Y_OFFSET) // Y_RATE

        move = i + j * GameRule.BOARD_HEIGHT

        if move in GameControl.available_action():

            GameControl.player_make_move(move)

            print(f"x={selected_x},y={selected_y},move={move}")

            if not GameControl.is_end():
                GameControl.ai_make_move(AI_NAME)

            update_board()


"""Display the selection box"""


def move_handler(event):
    selected_x = (event.x // X_RATE) * X_RATE + X_OFFSET
    selected_y = (event.y // Y_RATE) * Y_RATE + Y_OFFSET

    canvas.coords(selected, selected_x, selected_y)


"""Hide the selection box when the cursor leaves the canvas"""


def leave_handler(event):
    canvas.coords(selected, -100, -100)


canvas.bind('<Motion>', move_handler)
canvas.bind('<Leave>', leave_handler)
canvas.bind("<Button-1>", click_handler)

start()

root.mainloop()
