# Author: Bishal Sarang
from solve import Solution, start_config
from state import State


def main():
    # Create Solution Object
    s = Solution()
    # Start from start configureation
    start = start_config

    # Calculate level and manhattan distance for start config
    g, h = 0, s.calculate_manhattan_distance(start)

    # Make root State as start config
    root_state = State(g=g, h=h, parent=None, board=start)
    # Solve Recursively starting from root state
    s.solve(root_state)
    # Recolor the nodes and edges to show the path
    s.trace_path()
    # Write State space tree
    s.write_image("out.png")


if __name__ == '__main__':
    main()