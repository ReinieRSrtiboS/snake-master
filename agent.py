from queue import PriorityQueue
from random import randint

from gameobjects import GameObject
from move import Move, Direction


class Agent:
    snakeHeadX = 0
    snakeHeadY = 0
    food = (None,None)

    def get_move(self, board, score, turns_alive, turns_to_starve, direction):

        for x in range (0,25):  #TODO maak variabel
            for y in range (0,25):
                if board[x][y] == GameObject.SNAKE_HEAD:
                    self.snakeHeadX = x
                    self.snakeHeadY = y
                if board[x][y] == GameObject.FOOD:
                    self.food = (x,y)

        nextMove = None
        frontier = PriorityQueue()
        start = (self.snakeHeadX, self.snakeHeadY)
        frontier.put(start, 0)
        cost_so_far = {}
        came_from = {}
        cost_so_far[start] = 0
        came_from[start] = None

        while not frontier.empty():
            current = frontier.get()

            if current[0] is None or current[1] is None:
                continue

            if board[current[0]][current[1]] == GameObject.FOOD:
                nextMove = came_from[current]

                path = ""
                path += str(nextMove) + ", "
                while came_from[nextMove] is not None and came_from[nextMove] is not start and nextMove is not None:
                    nextMove = came_from[nextMove]
                    path += str(nextMove) + ", "
                break

            for next in self.children(board, current[0], current[1]):
                new_cost = cost_so_far[current] + 1
                if (next not in cost_so_far or new_cost < cost_so_far[next]) and next[0] is not None:
                    cost_so_far[next] = new_cost
                    frontier.put(next, new_cost + self.manhattanDistance(next[0], next[1]))
                    came_from[next] = current

        # if nextMove is None:
        #     moves = [Move.STRAIGHT, Move.LEFT, Move.RIGHT]
        #     return moves[randint(0,2)]
        # else:
        #     print(nextMove)

        return self.getDirection(direction, nextMove[0], nextMove[1])

    def children(self, board, x, y):    #TODO maak variabel
        available = [(None, None)] * 4
        if x + 1 < 25 and (board[x + 1][y] == GameObject.EMPTY or board[x + 1][y] == GameObject.FOOD):
            available[0] = (x + 1, y)
        if x - 1 >= 0 and (board[x - 1][y] == GameObject.EMPTY or board[x - 1][y] == GameObject.FOOD):
            available[1] = (x - 1, y)
        if y + 1 < 25 and (board[x][y + 1] == GameObject.EMPTY or board[x][y + 1] == GameObject.FOOD):
            available[2] = (x, y + 1)
        if y - 1 >= 0 and (board[x][y - 1] == GameObject.EMPTY or board[x][y - 1] == GameObject.FOOD):
            available[3] = (x, y - 1)
        return available

    def manhattanDistance(self, x, y):
        return abs(self.food[0] - x) + abs(self.food[1] - y)

    def getDirection(self, direction, x, y):
        difX = x - self.snakeHeadX
        difY = y - self.snakeHeadY

        if direction == Direction.NORTH and difY == -1:
            return Move.STRAIGHT
        if direction == Direction.NORTH and difX == 1:
            return Move.RIGHT
        if direction == Direction.NORTH and difX == -1:
            return Move.LEFT

        if direction == Direction.EAST and difY == 1:
            return Move.LEFT
        if direction == Direction.EAST and difY == -1:
            return Move.RIGHT
        if direction == Direction.EAST and difX == 1:
            return Move.STRAIGHT

        if direction == Direction.SOUTH and difY == 1:
            return Move.STRAIGHT
        if direction == Direction.SOUTH and difX == 1:
            return Move.LEFT
        if direction == Direction.SOUTH and difX == -1:
            return Move.RIGHT

        if direction == Direction.WEST and difY == -1:
            return Move.RIGHT
        if direction == Direction.WEST and difY == 1:
            return Move.LEFT
        if direction == Direction.WEST and difX == -1:
            return Move.STRAIGHT


    def on_die(self):
        """This function will be called whenever the snake dies. After its dead the snake will be reincarnated into a
        new snake and its life will start over. This means that the next time the get_move function is called,
        it will be called for a fresh snake. Use this function to clean up variables specific to the life of a single
        snake or to host a funeral.
        """
        pass
