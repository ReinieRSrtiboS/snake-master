from queue import PriorityQueue

from gameobjects import GameObject
from move import Move, Direction


class Agent:
    snakeHeadX = None
    snakeHeadY = None
    score = 0
    food = (None, None)

    def get_move(self, board, score, turns_alive, turns_to_starve, direction):

        if score is not self.score:
            self.score = score

        for x in range(0, 25):  # TODO make variable
            for y in range(0, 25):
                if board[x][y] == GameObject.SNAKE_HEAD:
                    self.snakeHeadX = x
                    self.snakeHeadY = y
                if board[x][y] == GameObject.FOOD:
                    self.food = (x, y)

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

            if board[current[0]][current[1]] == GameObject.FOOD:
                next_move = current

                path = ""
                path += str(next_move) + ", "
                while came_from[next_move] is not start:
                    next_move = came_from[next_move]
                    path += str(next_move) + ", "
                break

            if current is start:
                for child in self.children(board, current[0], current[1], direction):
                    new_cost = cost_so_far[current] + 1
                    if child not in cost_so_far or new_cost < cost_so_far[child]:
                        cost_so_far[child] = new_cost
                        frontier.put(child, new_cost + self.manhattan_distance(child[0], child[1]))
                        came_from[child] = current

            else:
                for child in self.children(board, current[0], current[1], self.get_new_direction(came_from[current][0], came_from[current][1], current[0], current[1])):
                    new_cost = cost_so_far[current] + 1
                    if child not in cost_so_far or new_cost < cost_so_far[child]:
                        cost_so_far[child] = new_cost
                        frontier.put(child, new_cost + self.manhattan_distance(child[0], child[1]))
                        came_from[child] = current

        # print(self.food)
        # print(path)
        return self.get_turn(direction, self.snakeHeadX, self.snakeHeadY, next_move[0], next_move[1])

    def children(self, board, x, y, direction):
        available = []
        for next in direction.get_xy_moves():
            if 25 > x + next[0] >= 0 and 25 > y + next[1] >= 0:     # TODO make variable
                if board[x + next[0]][y + next[1]] == GameObject.EMPTY or board[x + next[0]][y + next[1]] == GameObject.FOOD:
                    available.append((x + next[0], y + next[1]))

        return available

    def manhattan_distance(self, x, y):
        return abs(self.food[0] - x) + abs(self.food[1] - y)

    def get_turn(self, direction, old_x, old_y, new_x, new_y):      # TODO check if it's not mirrored
        dif_x = new_x - old_x
        dif_y = new_y - old_y

        for i in range(0, 4):
            if Direction(i).get_xy_manipulation() == (dif_x, dif_y):
                new_direction = Direction(i)

        return self.direction_to_move(direction, new_direction)

    def direction_to_move(self, old_direction, new_direction):
        for i in range(-1, 2):
            if old_direction.get_new_direction(Move(i)) == new_direction:
                return Move(i)
        raise ValueError("Unable to get to new square")

    def get_new_direction(self, old_x, old_y, new_x, new_y):
        dif_x = new_x - old_x
        dif_y = new_y - old_y

        for i in range(0, 4):
            if Direction(i).get_xy_manipulation() == (dif_x, dif_y):
                new_direction = Direction(i)

        return new_direction

    def on_die(self):
        raise ValueError("R.I.P.")
        pass
