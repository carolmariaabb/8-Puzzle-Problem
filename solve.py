import pydot
import os
from copy import deepcopy
from state import State

# Set it to bin folder of graphviz
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

# Start Board configuration
start_config = [[1, 8, 2],
                [-1, 4, 3],
                [7, 6, 5],
                ]

# Goal Board configuration
goal_config = [[1, 2, 3],
               [4, 5, 6],
               [7, 8, -1],
               ]

operators = {"L": (0, -1),
             "R": (0, 1),
             "U": (-1, 0),
             "D": (1, 0),
             }

# Dictionary that maps each element to its (row, col) in goal configuration
goal_position = {goal_config[row][col]: (row, col) for row in range(3) for col in range(3)}


class Solution(object):
    def __init__(self):
        self.graph = pydot.Dot(graph_type="digraph", bgcolor="#fff3af", strict=True, label="8 Puzzle Problem      ",
                               labelloc="top", labeljust="center", fontcolor="black", fontsize="40")
        self.visited = dict()
        self.goal = None

    def write_image(self, file_name: str = "out.png") -> object:
        """
        :param file_name: Name of the output file to be written
        """
        try:
            self.graph.write_png(file_name)
            print(f"Image {file_name} written successfully.")
        except Exception as e:
            print("Error Writing image", e)

    def draw_legend(self):
        """
            Utility method to draw legend on graph if  legend flag is ON
        """
        graphlegend = pydot.Cluster(graph_name="legend", label="Legend", fontsize="20", color="#fff3af",
                                    fontcolor="blue", style="filled", fillcolor="#fff3af")

        node1 = pydot.Node("1", style="filled", fillcolor="gold", label="g: depth level\n\n h: Manhattan Distance",
                           shape="plaintext", labeljust="left", fontsize="20", fontcolor="red", width="3")
        graphlegend.add_node(node1)

        node2 = pydot.Node("2", label="", shape="plaintext", fontsize="20", fontcolor="red", width="3")
        graphlegend.add_node(node2)

        graphlegend.add_edge(pydot.Edge("1", "2", style="invis"))
        self.graph.add_subgraph(graphlegend)

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
                next_state = State(g=g_current, h=h_current, parent=parent_state, board=deepcopy(board_parent))
                self.graph.add_node(next_state.node)

                # Draw edge from parent node to next generated node
                edge = pydot.Edge(parent_state.node_name, next_state.node_name, label=f" {direction}", fontsize="24")
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
        path = list()
        while self.goal.parent:
            # TODO: Recolor the node
            # Make Edge
            edge = pydot.Edge(self.goal.parent.node_name, self.goal.node_name, style="filled", color="red", penwidth=3,
                              fontsize="24")
            self.graph.add_edge(edge)

            path.append(self.goal.parent)
            self.goal = self.goal.parent

        # Show solution states on console
        path = path[::-1]
        print("The solution states are shown below\n")
        print(f"""| {start_config[0][0]} | {start_config[0][1]} | {start_config[0][2]} |\n| {start_config[1][0]} | {
        start_config[1][1]} | {start_config[1][2]} |\n| {start_config[2][0]} | {start_config[2][1]} | {start_config[2][
            2]} |""", end="\n\n")
        for state in path:
            print(state, end="\n\n")

    @staticmethod
    def calculate_manhattan_distance(board):
        dist = 0
        for row in range(3):
            for col in range(3):
                if board[row][col] != -1:
                    x, y = goal_position[board[row][col]]
                    dist += abs(x - row) + abs(y - col)
        return dist
