# Author: Bishal Sarang
from solve import *
from state import State
import pydot


def main():
    s = Solution()

    start = start_config
    g, h = 0, s.calculate_manhattan_distance(start)
    root_state = State(g=g, h=h, parent=None, board=start)
    s.solve(root_state)
    s.trace_path()
    s.write_image("out.png")
    pass


if __name__ == '__main__':
    main()
