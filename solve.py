import pydot
from collections import deque
from copy import deepcopy
from state import State

# Start Board configuration
start_config = [[2, 8, 3],
                [1, 6, 4],
                [7, -1, 5],
                ]

# Goal Board configuration
goal_config = [[1, 2, 3],
               [8, -1, 4],
               [7, 6, 5],
               ]

operators = {"L": (0, -1),
             "R": (0, 1),
             "U": (-1, 0),
             "D": (1, 0),
             }


class Solution(object):
    def __init__(self):
        self.graph = pydot.Dot(graph_type="digraph", strict=True)
        self.visited = dict()
        self.goal = None

    def write_image(self, file_name="out.png"):
        self.graph.write_png("out.png")

    @staticmethod
    def find_blank_position(board):
        for i in range(3):
            for j in range(3):
                if board[i][j] == -1:
                    return i, j

    @staticmethod
    def is_valid_move(next_x, next_y):
        return 0 <= next_x < 3 and 0 <= next_y < 3

    def solve(self, parent_state):
        f_parent, g_parent, h_parent, board_parent, node_parent = parent_state.f, parent_state.g, parent_state.h, parent_state.board, parent_state.node

        if parent_state.is_start_state(start_config):
            self.graph.add_node(node_parent)

        self.visited[parent_state] = True
        if parent_state.is_goal_state(goal_config):
            self.goal = parent_state
            self.graph.add_node(node_parent)
            return True

        current_x, current_y = self.find_blank_position(board_parent)
        solved = False
        minm_heuristic_distance = float("inf")
        selected_board_configuration = None

        for direction, (x, y) in operators.items():
            next_x, next_y = current_x + x, current_y + y

            if self.is_valid_move(next_x, next_y):
                board_parent[next_x][next_y], board_parent[current_x][current_y] = board_parent[current_x][current_y], \
                                                                                   board_parent[next_x][next_y]

                g_current, h_current = g_parent + 1, self.calculate_manhattan_distance(board_parent)

                next_state = State(g=g_current, h=h_current, parent=parent_state, board=board_parent)
                self.graph.add_node(next_state.node)

                edge = pydot.Edge(parent_state.node_name, next_state.node_name, label=f" {direction}")
                self.graph.add_edge(edge)

                f = g_current + h_current

                if next_state not in self.visited and f < minm_heuristic_distance:
                    minm_heuristic_distance = f
                    selected_board_configuration = deepcopy(next_state)

                board_parent[next_x][next_y], board_parent[current_x][current_y] = board_parent[current_x][current_y], \
                                                                                   board_parent[next_x][next_y]

        if selected_board_configuration is not None:
            solved = self.solve(selected_board_configuration)

        return solved

    def trace_path(self):
        i = 0
        while self.goal.parent:
            # Connect every 2 nodes in path by recoloring the node
            u = pydot.Node(self.goal.parent.node_name, label=self.goal.parent.generate_label("gold"))
            self.graph.add_node(u)
            v = pydot.Node(self.goal.node_name, label=self.goal.parent.generate_label("gold"))
            self.graph.add_node(v)

            # Make Edge
            edge = pydot.Edge(self.goal.parent.node_name, self.goal.node_name, style="filled", color="red", penwidth=3)
            self.graph.add_edge(edge)

            self.goal = self.goal.parent
            i += 1

    @staticmethod
    def calculate_manhattan_distance(board):
        """Returns Manhattan distance for the board configuration   

        Arguments:
            board {[[int]]} -- [2D matrix of 3 * 3 i.e current board configuration]

        Returns:
            [int] -- [Calculate Manhattan distance]
        """

        def is_valid_move(next_x, next_y):
            return 0 <= next_x < 3 and 0 <= next_y < 3

        def bfs(i, j):
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
                if board[i][j] == goal_config[u_i][u_j]:
                    return u_l
                for direction, (x, y) in operators.items():
                    next_x, next_y, next_l = u_i + x, u_j + y, u_l + 1

                    if is_valid_move(next_x, next_y):
                        if (next_x, next_y) not in visited:
                            visited[(next_x, next_y)] = True
                            q.append((next_x, next_y, next_l))

        # Returns the manhattan distance i.e the sum of number of minimum steps to reach
        # goal position
        return sum(bfs(i, j) for i in range(3) for j in range(3) if board[i][j] != -1)
