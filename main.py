from typing import Union
import random

class TikTakToe:
    def __init__(self) -> None:
        self.gameboard = None
        self.turn = None
        self.ai = False
        self.mark = ["○", "x"]
        # dia_1 and dia_2 are used for diagonal check.
        self.dia_1 = set([(0, 0), (1, 1), (2, 2)])
        self.dia_2 = set([(0, 2), (1, 1), (2, 0)])

    def reset_gameboard(self) -> None:
        """This function is for generates/resets the gameboard. The gameboard is a nested list."""
        self.gameboard = [
            [0, 1, 2], 
            [3, 4, 5], 
            [6, 7, 8]
        ]
        self.turn = -1
        self.ai = False

    def main_menu(self) -> None:
        """This function starts/restarts this game."""
        self.reset_gameboard()
        opt = input("Welcome to Tic Tac Toe!\n'a': Play with AI. 'any other keys': Play with player 2.\n")
        if opt.lower() == "a":
            self.ai = True
        self.game()
        
    def display(self) -> None:
        """This function prints the current gameboard."""
        print() # print an empty line for seperating each turn.
        for sublist in self.gameboard:
            print(f"{self.display_helper(sublist[0])} | {self.display_helper(sublist[1])} | {self.display_helper(sublist[2])}")
            
    def display_helper(self, element: Union[str, int]) -> str:
        """This function checks if the element is an integer or mark, and converts the number from 0-8 to 1-9."""
        return str(element + 1) if isinstance(element, int) else element
    
    def locator(self, num: int) -> tuple:
        """This function converts the user input to the (row, col) of the nested list (game-board)."""
        row, col = (num - 1) // 3, (num - 1) % 3
        return row, col

    def check_diagonal(self, alist: list) -> list:
        """This function helps if the player/AI has a diagonal line."""
        return [self.gameboard[row][col] for row, col in alist]

    def terminate(self, turn: int, player: int) -> int:
        """return 1 if the player/AI win. return 0 if draw. return -1 if not terminate."""
        # horizontal check
        for row in range(3):
            if set(self.gameboard[row]) == {self.mark[player]}:
                return 1
        # vertical check
        for col in zip(self.gameboard[0], self.gameboard[1], self.gameboard[2]):
            if set(col) == {self.mark[player]}:
                return 1
        # diagonal check
        if set([self.gameboard[row][col] for row, col in self.dia_1]) == {self.mark[player]}:
            return 1
        if set([self.gameboard[row][col] for row, col in self.dia_2]) == {self.mark[player]}:
            return 1
        # draw
        if turn == 8:
            return 0
        return -1
    
    def player_move(self, player: int) -> None:
        """This function outputs the AI move or asks the player inputs their move."""
        if self.ai is True and player == 1:
            next_move = self.ai_move(self.gameboard) + 1
            print(f"AI placed {self.mark[player]} on {next_move}.")
        else:
            valid_move = [num + 1 for sublist in self.gameboard for num in sublist if isinstance(num, int)]
            while True:
                next_move = input(f"Player {player + 1}'s turn. Please place {self.mark[player]} on the number:")
                if next_move.isdigit() and int(next_move) in valid_move:
                    break
                else:
                    self.display()
                    print(f"Invalid move. Please input a number in {valid_move}.\n")
            print(f"Player {player + 1} placed {self.mark[player]} on {next_move}.")
        row, col = self.locator(int(next_move))
        self.gameboard[row][col] = self.mark[player]
        
    def ai_move(self, gameboard: list) -> int:
        """This function provides AI move."""
        # difficulty: easy
        # return random.choice([element + 1 for sublist in self.gameboard for element in sublist if isinstance(element, int)])

        # difficulty: hard
        best_move, best_score = None, float("-inf")
        for move in [element for sublist in gameboard for element in sublist if isinstance(element, int)]:
            row, col = self.locator(move + 1)
            gameboard[row][col] = "x"
            score = self.minimax(self.turn, gameboard)
            if score > best_score:
                best_move, best_score = move, score
            gameboard[row][col] = move
        return best_move

    def minimax(self, turn: int, gameboard: list) -> int:
        """AI win: 1, player win: -1, tie: 0"""
        player = turn % 2
        result = self.terminate(turn, player)
        if result == 0:
            return 0
        elif result == 1:
            if player == 1:
                return 1
            else:
                return -1

        turn += 1
        # min
        if turn % 2 == 0:
            score = float("inf")
            for move in [element for sublist in gameboard for element in sublist if isinstance(element, int)]:
                row, col = self.locator(move + 1)
                gameboard[row][col] = "○"
                score = min(self.minimax(turn, gameboard), score)
                gameboard[row][col] = move
        # max
        else:
            score = float("-inf")
            for move in [element for sublist in gameboard for element in sublist if isinstance(element, int)]:
                row, col = self.locator(move + 1)
                gameboard[row][col] = "x"
                score = max(self.minimax(turn, gameboard), score)
                gameboard[row][col] = move
        #turn -= 1
        return score

    def game(self):
        """main function of this game."""
        while True:
            self.turn += 1
            self.display()
            player = self.turn % 2
            self.player_move(player)
            game_state = self.terminate(self.turn, player)
            if game_state == 1:
                self.display()
                if player == 1 and self.ai == True:
                    print("Player AI ('x') win.")
                else:
                    print(f"Player {player + 1} ({self.mark[player]}) win.")
                break
            elif game_state == 0:
                self.display()
                print(f"Draw!\n")
                break
        again = input("'r': Try again! 'any other keys': quit")
        if again.lower() == 'r':
            self.main_menu()

play = TikTakToe()
play.main_menu()
