import GameRule
import random

ALPHA = 0.9
GAMMA = 1

"""
Turn the <state> into hashable keys to store in memory of GameAI
"""


def state_to_hash(state):
    hash = ""
    for place in state:
        hash += str(place)

    return hash


class GameAI:
    """
    Initialize AI with given brain/memory (as .json file)
    """

    def __init__(self, brain):
        self.memory = brain

    """
    Return the best move with given <state>. 
    """

    def pick_move(self, state, rand=True):

        if GameRule.player(state) == GameRule.PLAYER1:
            # Used to record the lowest q-value
            val = 2
            # Indicate the player in turn as the result of function
            # GameRule.is_end()
            turn = -1
        else:
            val = -2
            turn = 1

        # Store the move to be returned
        move = -1

        # Find the best act to return
        for act in GameRule.actions(state):
            # Simulate that <act> is taken as a move
            state_cpy = state.copy()
            GameRule.make_move(state_cpy, act)

            # See if <act> is an end move.
            finished, winner = GameRule.is_end(state_cpy)
            if finished:
                # Return the <act> if this act leads to victory
                if winner == turn:
                    return act
                # TODO: Debatable:
                # If <act> does not lead to victory but end the game
                else:
                    return act
            else:
                # If <act> is not an end move, evaluate the q-value of <act>
                temp = self.q_eval_unfinished(state, act)

            # Find the <act> with minimum score if AI went first
            if GameRule.player(state) == GameRule.PLAYER1:
                if temp < val:
                    val = temp
                    move = act

            # Find the <act> with the maximum score otherwise
            else:
                if temp > val:
                    val = temp
                    move = act

            # Added some pseudo-randomness when picking the move
            if rand:
                stochastic = random.choice([True, False])
                if stochastic:
                    if temp == val:
                        val = temp
                        move = act

        return move

    """
    Return the q-value of the given <action> of the given <state>.
    
    If the state is never encountered before, create the state in memory and 
    return 0.
    """

    def q_eval_unfinished(self, state, action):
        state_hash = state_to_hash(state)

        # Fetch the q-value if the <state> is encountered before
        if state_hash in self.memory:
            return self.memory[state_hash][str(action)]

        else:
            self.memory[state_hash] = {}
            for a in GameRule.actions(state):
                self.memory[state_hash][str(a)] = 0
            return 0

    """
    Used when the game is finished. Record the reward and update the q-value of
    states in <history>.
    """

    def q_eval_finished(self, state, history):

        finished, score = GameRule.is_end(state)

        if not finished:
            print("Big Error")

        state_copy = state.copy()
        last_act = history[-1]

        state_copy[last_act] = 0
        state_copy_hash = state_to_hash(state_copy)

        # Update the score of the last move before finished
        if state_copy_hash not in self.memory:
            self.memory[state_copy_hash] = {}
            for a in GameRule.actions(state_copy):
                self.memory[state_copy_hash][str(a)] = 0
        self.memory[state_copy_hash][str(last_act)] = score

        # Update the q-value of each action in <history>
        for i in range(len(history) - 2, -1, -1):

            # Simulate that the <act> is not taken yet.
            state_after = state_copy.copy()
            act = history[i]
            state_copy[act] = 0
            state_copy_hash = state_to_hash(state_copy)

            # Find that simulated state <state_copy> in memory
            if state_copy_hash not in self.memory:
                self.memory[state_copy_hash] = {}
                for a in GameRule.actions(state_copy):
                    self.memory[state_copy_hash][str(a)] = 0
            old_estimate = self.memory[state_copy_hash][str(act)]

            # Find the future estimate of <state_copy> taking action <act>
            all_moves_score = []

            # <state_after> is the state that <state_copy> takes action <act>
            for move in GameRule.actions(state_after):
                all_moves_score.append(
                    self.q_eval_unfinished(state_after, move))

            if GameRule.player(state_copy) == GameRule.PLAYER1:

                # Because PLAYER2 goes for the highest score, so we will use the
                # maximum to represent this state for PLAYER1
                future_estimate = max(all_moves_score)
            else:
                future_estimate = min(all_moves_score)

            # A formula to evaluate q-values
            self.memory[state_copy_hash][str(act)] = old_estimate + ALPHA * (
                    GAMMA * future_estimate - old_estimate)

        return score
