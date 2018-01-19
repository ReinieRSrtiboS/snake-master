from queue import PriorityQueue

import sys

from gameobjects import GameObject
from move import Move, Direction


class Agent:
    snakeHeadX = None
    snakeHeadY = None
    score = 0
    food = []

    def get_move(self, board, score, turns_alive, turns_to_starve, direction):

        # Initialise
        for x in range(0, 25):  # TODO make variable
            for y in range(0, 25):
                if board[x][y] == GameObject.SNAKE_HEAD:
                    self.snakeHeadX = x
                    self.snakeHeadY = y
                if board[x][y] == GameObject.FOOD and not self.food.__contains__((x,y)):
                    self.food.append((x, y))

        if score is not self.score: # TODO implement something smart
            self.score = score
            self.food.remove((self.snakeHeadX, self.snakeHeadY))

        next_move = None
        frontier = PriorityQueue()
        start = (self.snakeHeadX, self.snakeHeadY)
        frontier.put(start, self.manhattan_distance(self.snakeHeadX, self.snakeHeadY))
        cost_so_far = {}
        came_from = {}
        cost_so_far[start] = 0
        came_from[start] = None

        while not frontier.empty():
            current = frontier.get()

            # If food is found look up the path stored in came_from
            if board[current[0]][current[1]] == GameObject.FOOD:
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
                        frontier.put(child, new_cost + self.manhattan_distance(child[0], child[1]))
                        came_from[child] = current

            else:
                # The same as above but the direction has to be calculated
                for child in self.children(board, current[0], current[1], self.get_new_direction(came_from[current][0], came_from[current][1], current[0], current[1])):
                    new_cost = cost_so_far[current] + 1
                    if child not in cost_so_far or new_cost < cost_so_far[child]:
                        cost_so_far[child] = new_cost
                        frontier.put(child, new_cost + self.manhattan_distance(child[0], child[1]))
                        came_from[child] = current

        print(self.food)
        print(path)
        if next_move is None:
            return Move.STRAIGHT
        return self.get_turn(direction, self.snakeHeadX, self.snakeHeadY, next_move[0], next_move[1])

    # Returns all the possible locations the snake can move to
    def children(self, board, x, y, direction):
        available = []
        for next in direction.get_xy_moves():
            if 25 > x + next[0] >= 0 and 25 > y + next[1] >= 0:     # TODO make variable
                if board[x + next[0]][y + next[1]] == GameObject.EMPTY or board[x + next[0]][y + next[1]] == GameObject.FOOD:
                    available.append((x + next[0], y + next[1]))

        return available

    # Calculates the Manhatten distance to the closest food
    def manhattan_distance(self, x, y):
        distance = sys.maxsize
        for food in self.food:
            if abs(food[0] - x) + abs(food[1] - y) < distance:
                distance = abs(food[0] - x) + abs(food[1] - y)
        return distance

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

    # If the snake dies, throw error for a moment of silence
    def on_die(self):
        raise ValueError("R.I.P.")
        pass
