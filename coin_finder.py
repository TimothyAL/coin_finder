import enum
import random
import sys
import os

os.system('color')

class GameEndingException(Exception):
    pass

class Direction(enum.Enum):
    RIGHT = 'right'
    LEFT = 'left'

cord = (int, int, Direction)

class Move(enum.Enum):
    AHEAD = 'ahead'
    DOWN = 'down'

current_location: cord = (0,0, Direction.RIGHT)


def build_matrix(x: int, y:int):
    matrix = []
    for i in range(y):
        matrix_row = []
        for j in range(x):
            matrix_row.append(random.choice(['C', '#', 'E']))
        matrix.append(matrix_row)
    return matrix


def move(current_location: cord, choice: Move, matrix):
    x = current_location[0]
    y = current_location[1]
    looking = current_location[2]
    print(f'Chose move {choice.value}')
    try:
        if choice == Move.DOWN:
            if looking == Direction.RIGHT:
                looking = Direction.LEFT
            else:
                looking = Direction.RIGHT
            return(x, y+1, looking)
        else:
            if looking == Direction.RIGHT:
                if x+1 >= len(matrix[y]):
                    raise IndexError
                return (x+1, y, Direction.RIGHT)
            if x-1 < 0:
                raise IndexError
            return (x-1, y, Direction.LEFT)
    except IndexError:
        raise IndexError

def did_score(matrix, location: cord):
    if matrix[location[1]][location[0]] == 'C':
        return True
    elif matrix[location[1]][location[0]] == 'E':
        return False
    else:
        raise GameEndingException

def print_location(matrix, current_location):
    local_matrix = matrix
    if local_matrix[current_location[1]][current_location[0]] == "#" and not (current_location[0] == 0 and current_location[1] == 0):
        local_matrix[current_location[1]][current_location[0]] = "\033[91m#\033[0m"
    else:
        local_matrix[current_location[1]][current_location[0]] = '\033[94mX\033[0m'
    print(f'you are at \033[94m({current_location[0]},{current_location[1]})\033[0m and you are looking \033[94m{current_location[2].value}\033[0m')
    for row in range(len(local_matrix)):
        for loc in range(len(local_matrix[row])):
            print(local_matrix[row][loc], end="  ")
        print()

def game_loop(matrix):
    points: int = 0
    current_location: cord = (0, 0, Direction.RIGHT)
    try:
        print("\n\nWelcome to Coin Finder\n")
        while True:
            print(f'you currently have \033[94m{points}\033[0m points and the board looks like:')
            try:
                print_location(matrix, current_location)
                choice = input(f'How Would you like to move?\n1 = Down   or   2 = {current_location[2].value}: ')
                choice = int(choice)
                if choice == 1:
                    choice = Move.DOWN
                else:
                    choice = Move.AHEAD
                current_location = move(current_location, choice, matrix)
                if did_score(matrix, current_location):
                    points += 1
            except (IndexError, TypeError):
                end_game = input('that was not a valid move would you like to try again? 1:yes, any other key: no   ')
                if end_game != "1":
                    raise GameEndingException
    except GameEndingException:
        try:
            print_location(matrix, current_location)
        except IndexError:
            pass
        finally:
            print(f'You landed on a \"#\" or ended the game you earned {points} points')
            print("thanks for playing")

def setup_game(max_x: int=15, max_y: int=20):
    matrix = build_matrix(max_x, max_y)
    game_loop(matrix)

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1].isnumeric() and sys.argv[2].isnumeric():
        setup_game(max_x=int(sys.argv[1]), max_y=int(sys.argv[2]))
    else:
        setup_game()