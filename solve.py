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

    def write_image(self, file_name: str = "out.png") -> object:
        """
        :param file_name: Name of the output file to be written
        """
        self.graph.write_png(file_name)

    @staticmethod
    def find_blank_position(board) -> (int, int):
        """
        :param board: 3 * 3 board config
        :return: (i, j) the position of blank
        """
        for i in range(3):
            for j in range(3):
                if board[i][j] == -1:
                    return i, j

    @staticmethod
    def is_valid_move(row: int, col: int) -> bool:
        """
        Checks if the move is valid i.e no boundary is crossed
        :param row: row number
        :param col: col_number
        :return:
        """
        return 0 <= row < 3 and 0 <= col < 3

    def solve(self, parent_state: State) -> bool:
        # Extract all the parameters f, g, h, board, node of parent
        f_parent, g_parent, h_parent, board_parent, node_parent = parent_state.f, parent_state.g, parent_state.h, parent_state.board, parent_state.node

        if parent_state.is_start_state(start_config):
            self.graph.add_node(node_parent)

        # Mark parent_state as visited
        self.visited[parent_state] = True

        if parent_state.is_goal_state(goal_config):
            self.goal = parent_state
            self.graph.add_node(node_parent)
            return True

        # Find blank position in current board config
        current_row, current_col = self.find_blank_position(board_parent)

        # Initially for this state it is not solved and minimum heuristic distance is infinite and none of chil board config is selected
        solved = False
        minm_heuristic_distance = float("inf")
        selected_board_configuration = None

        # Apply operations
        for direction, (offset_row, offset_col) in operators.items():
            # Find next row and column position
            next_row, next_col = current_row + offset_row, current_col + offset_col

            if self.is_valid_move(next_row, next_col):
                # Move the blank i.e swap the position
                board_parent[next_row][next_col], board_parent[current_row][current_col] = board_parent[current_row][
                                                                                               current_col], \
                                                                                           board_parent[next_row][
                                                                                               next_col]

                # Find level and manhattan distance for new board configuration
                g_current, h_current = g_parent + 1, self.calculate_manhattan_distance(board_parent)

                # Make next State object and add node to the solution graph
                next_state = State(g=g_current, h=h_current, parent=parent_state, board=board_parent)
                self.graph.add_node(next_state.node)

                # Draw edge from parent node to next generated node
                edge = pydot.Edge(parent_state.node_name, next_state.node_name, label=f" {direction}")
                self.graph.add_edge(edge)

                f = g_current + h_current
                # If f is less than minimum heuristic distance obtained so far
                if next_state not in self.visited and f < minm_heuristic_distance:
                    minm_heuristic_distance = f
                    selected_board_configuration = deepcopy(next_state)

                board_parent[next_row][next_col], board_parent[current_row][current_col] = board_parent[current_row][
                                                                                               current_col], \
                                                                                           board_parent[next_row][
                                                                                               next_col]

        # If at least one board is valid, solve recursively for best(minimum f) valid next configuration
        if selected_board_configuration is not None:
            solved = self.solve(selected_board_configuration)

        return solved

    def trace_path(self) -> None:
        """
        Show solution nodes by recoloring
        """
        i = 0
        while self.goal.parent:
            # Connect every 2 nodes in path by recoloring the node
            # u = pydot.Node(self.goal.parent.node_name, label=self.goal.parent.generate_label("gold"))
            # self.graph.add_node(u)
            # v = pydot.Node(self.goal.node_name, label=self.goal.generate_label("gold"))
            # self.graph.add_node(v)

            # Make Edge
            edge = pydot.Edge(self.goal.parent.node_name, self.goal.node_name, style="filled", color="red", penwidth=3)
            self.graph.add_edge(edge)

            self.goal = self.goal.parent
            i += 1

    @staticmethod
    def calculate_manhattan_distance(board):

        def is_valid_move(row, col):
            return 0 <= row < 3 and 0 <= col < 3

        def bfs(row, col):
            """"BFS helper function to calculate the shortest distance for a value to reach
                its correct place
            """
            q = deque()
            visited = dict()

            # Tuple (x_pos, y_pos, depth_level)
            q.append((row, col, 0))
            visited[(row, col)] = True

            while q:
                current_row, current_col, current_level = q.popleft()
                if board[row][col] == goal_config[current_row][current_col]:
                    return current_level
                for direction, (x, y) in operators.items():
                    next_row, next_col, next_level = current_row + x, current_col + y, current_level + 1

                    if is_valid_move(next_row, next_col):
                        if (next_row, next_col) not in visited:
                            visited[(next_row, next_col)] = True
                            q.append((next_row, next_col, next_level))

        # Returns the manhattan distance i.e the sum of number of minimum steps to reach
        # goal position
        return sum(bfs(row, col) for row in range(3) for col in range(3) if board[row][col] != -1)
