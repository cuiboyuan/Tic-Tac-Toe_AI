# Tic-Tac-Toe_AI
## Brief Intro
An AI for the game Tic-Tac-Toe. Consisting both codes for Training an AI and player playing against AI. AI will learning through games with players and store the knowledge as json file.
The project uses the reinforcement learning to train the AI, specifically the Q-learning method.

## File Description

### Game_GUI.py
This file is the where the program runs. User can play Tic-Tac-Toe game against AI with a graphic user interface made by Tkinter library. 

### Play.py
This file has the same function as Game_GUI.py except that there is no beautiful GUI. The user will have to play against AI in command prompt.

### Training.py
This file is for the training of AIs. User can load two AIs to let them play against each other to improve both AIs' knowledge (add more information to the json files.)

### Master_Training.py
This is the other training method. Different from Training.py, user can only load one AI at a time, and the AI (refer as "student") will be trained against a "Master" AI ([Master.py](master.py)). The Master AI will always pick the best move in every game, so it is expected that the Student AI will mimic the move of Master and improve faster.

### Master.py
User cannot directly run this file. This file consists of a function that perfectly predict every possible outcome of the Tic-Tac-Toe game. It will pick the best move every time. The function is implemented by recursive logics instead of reinforcement learning. Theoretically, you can never beat this one in a Tic-Tac-Toe game (That's why it is called Master).

### GameControl.py
User cannot directly run this file. The “Train Station” of this program which handles input from front ends and gives back the result from back end.

### GameAI.py
Where the magic happens. The GameAI will provide the "best" move (in its opinion) with the given Tic-Tac-Toe game board. Record and update its knowledge every time the game ends.

### GameRule.py
Consist of basic rule of Tic-Tac-Toe, such as who is the winner, what actions are available, whether the game has ended, etc.

### brains
Consist of all the AIs' knowledge, i.e. json files

### images
Consists of all images used by [Game_GUI.py](#game_gui.py)
