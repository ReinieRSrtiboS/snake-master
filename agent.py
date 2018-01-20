from queue import PriorityQueue

import sys

from gameobjects import GameObject
from move import Move, Direction


class Agent:
    snakeHeadX = None
    snakeHeadY = None
    score = 0
    food = []
    copy_board = [[0] * 25] * 25

    def get_move(self, board, score, turns_alive, turns_to_starve, direction):

        # Initialise
        for x in range(0, len(board)):
            for y in range(0, len(board[0])):
                if board[x][y] == GameObject.SNAKE_HEAD:
                    self.snakeHeadX = x
                    self.snakeHeadY = y
                if board[x][y] == GameObject.FOOD and (x, y) not in self.food:
                    self.food.append((x, y))

        if score is not self.score:
            self.score = score
            self.update_copy(self.snakeHeadX, self.snakeHeadY, True)
            if score > 0:
                self.food.remove((self.snakeHeadX, self.snakeHeadY))
        else:
            self.update_copy(self.snakeHeadX, self.snakeHeadY)

        next_move = self.a_star(board, direction, self.snakeHeadX, self.snakeHeadY)

        if next_move is None:
            next_move = self.a_star(board, direction, self.snakeHeadX, self.snakeHeadY, True)
            if next_move is None:
                return Move.STRAIGHT
            return next_move

        # print(self.food)
        # print(self.manhattan_distance(self.snakeHeadX, self.snakeHeadY))
        # print(path)

        return self.get_turn(direction, self.snakeHeadX, self.snakeHeadY, next_move[0], next_move[1])

    def a_star(self, board, direction, x, y, tail=False):
        next_move = None
        frontier = PriorityQueue()
        start = (x, y)
        frontier.put((self.manhattan_distance_to_food(x, y), start))
        cost_so_far = {}
        came_from = {}
        cost_so_far[start] = 0
        came_from[start] = None
        tail_x, tail_y = None, None

        if tail:
            copy = ""
            for i in range(0, 25):
                for j in range(0, 25):
                    copy += str(self.copy_board[i][j]) + " "
                    if self.copy_board[i][j] == 1:
                        tail_x, tail_y = i, j
                copy += "\n"
            print(copy)

        while not frontier.empty():
            current = frontier.get()[1]

            # If food is found look up the path stored in came_from
            if board[current[0]][current[1]] == GameObject.FOOD or (tail and current[0] == tail_x and current[1] == tail_y):
                next_move = current

                path = ""
                path += str(next_move) + ", "
                while came_from[next_move] is not start:
                    next_move = came_from[next_move]
                    path += str(next_move) + ", "
                break

            # For all the possible moves from current
            if current is start:
                for child in self.children(board, current[0], current[1], direction):
                    new_cost = cost_so_far[current] + 1
                    # Checks whether this child is already been looked at and updates it if it found a faster route
                    if child not in cost_so_far or new_cost < cost_so_far[child]:
                        cost_so_far[child] = new_cost
                        if tail:
                            frontier.put((new_cost + self.manhattan_distance_to_tail(child[0], child[1], tail_x, tail_y), child))
                        else:
                            frontier.put((new_cost + self.manhattan_distance_to_food(child[0], child[1]), child))
                        came_from[child] = current

            else:
                # The same as above but the direction has to be calculated
                for child in self.children(board, current[0], current[1], self.get_new_direction(came_from[current][0], came_from[current][1], current[0], current[1])):
                    new_cost = cost_so_far[current] + 1
                    if child not in cost_so_far or new_cost < cost_so_far[child]:
                        cost_so_far[child] = new_cost
                        if tail:
                            frontier.put((new_cost + self.manhattan_distance_to_tail(child[0], child[1], tail_x, tail_y), child))
                        else:
                            frontier.put((new_cost + self.manhattan_distance_to_food(child[0], child[1]), child))
                        came_from[child] = current
        return next_move


    # Returns all the possible locations the snake can move to
    def children(self, board, x, y, direction):
        available = []
        for next in direction.get_xy_moves():
            if len(board) > x + next[0] >= 0 and len(board[0]) > y + next[1] >= 0:
                if board[x + next[0]][y + next[1]] == GameObject.EMPTY or board[x + next[0]][y + next[1]] == GameObject.FOOD:
                    available.append((x + next[0], y + next[1]))

        return available

    # Calculates the Manhatten distance to the closest food
    def manhattan_distance_to_food(self, x, y):
        distance = sys.maxsize
        for food in self.food:
            if abs(food[0] - x) + abs(food[1] - y) < distance:
                distance = abs(food[0] - x) + abs(food[1] - y)
        return distance

    # Calculates the Manhatten distance to the tail of the snake
    def manhattan_distance_to_tail(self, x, y, tail_x, tail_y):
        return abs(x - tail_x) + abs(y - tail_y)

    # Looks up how to move into the new position
    def get_turn(self, direction, old_x, old_y, new_x, new_y):
        dif_x = new_x - old_x
        dif_y = new_y - old_y

        for i in range(0, 4):
            if Direction(i).get_xy_manipulation() == (dif_x, dif_y):
                new_direction = Direction(i)

        for i in range(-1, 2):
            if direction.get_new_direction(Move(i)) == new_direction:
                return Move(i)
        raise ValueError("Unable to get to new square")

    # Gives the direction the snake moved
    def get_new_direction(self, old_x, old_y, new_x, new_y):
        dif_x = new_x - old_x
        dif_y = new_y - old_y

        for i in range(0, 4):
            if Direction(i).get_xy_manipulation() == (dif_x, dif_y):
                new_direction = Direction(i)

        return new_direction

    # Keeps track of the snake on the board
    def update_copy(self, x, y, ate=False):
        print(str(x) + " " + str(y))
        self.copy_board[x][y] = self.score + 2
        print(self.copy_board[x][y])
        if not ate:
            board = ""
            for i in range(0, 25):
                for j in range(0, 25):
                    if self.copy_board[i][j] > 0:
                        print(str(i) + " " + str(j))
                        self.copy_board[i][j] -= 1
                    board += str(self.copy_board[i][j]) + " "
                board += "\n"
            print(board)
        print(self.copy_board[x][y])

    # If the snake dies, throw error for a moment of silence
    def on_die(self):
        self.copy_board = [[0] * 25] * 25
        raise ValueError("R.I.P.    Simon de kekke snek")
        pass
