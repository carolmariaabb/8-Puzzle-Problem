import pydot
from collections import deque
from copy import deepcopy
import re


class State():
    def __init__(self):
        pass


class Solution(object):

    start_state = [[2, 8, 3],
                   [1, 6, 4],
                   [7, -1, 5],
                   ]

    goal_state = [[1, 2, 3],
                  [8, -1, 4],
                  [7, 6, 5],
                  ]

    operators = {"L": (0, -1),
                 "R": (0, 1),
                 "U": (-1, 0),
                 "D": (1, 0),
                 }

    visited, parent, g_and_h_value, node_list = dict(), dict(), dict(), dict()
    parent[tuple(map(tuple, start_state))] = None

    def __init__(self):
        pass

    def is_valid_move(self, next_x, next_y):
        return 0 <= next_x < 3 and 0 <= next_y < 3

    def is_goal_state(self, board):
        return all(board[i][j] == goal_state[i][j] for i in range(3) for j in range(3))

    def is_start_state(self, board):
        return all(board[i][j] == start_state[i][j] for i in range(3) for j in range(3))

    def calculate_manhattan_distance(self, board):
        """Returns Manhattan distance for the board configuration   

        Arguments:
            board {[[int]]} -- [2D matrix of 3 * 3 i.e current board configuration]

        Returns:
            [int] -- [Calculate Manhattan distance]
        """
        def bfs(board, i, j):
            """"BFS helper function to calculate the shortest distance for a value to reach 
                its correct place
            """

            q = deque()
            # Tuple (x_pos, y_pos, depth_level)
            q.append((i, j, 0))
            visited = dict()

            visited[(i, j)] = True
            while q:
                u_i, u_j, u_l = q.popleft()
                if board[i][j] == goal_state[u_i][u_j]:
                    return u_l
                for direction, (x, y) in operators.items():
                    next_x, next_y, next_l = u_i + x, u_j + y, u_l + 1

                    if is_valid_move(next_x, next_y):
                        if (next_x, next_y) not in visited:
                            visited[(next_x, next_y)] = True
                            q.append((next_x, next_y, next_l))

        # Returns the manhattan distance i.e the sum of number of minimum steps to reach
        # goal position
        return sum(bfs(board, i, j) for i in range(3) for j in range(3) if board[i][j] != -1)
