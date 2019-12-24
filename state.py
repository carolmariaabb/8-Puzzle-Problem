import pydot
import re
from string import  Template

class State(object):
    def __init__(self, *, g, h, parent, board):
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.parent = parent
        self.board = board
        self.node_name = str(tuple(map(tuple, self.board))) + str(self.g)
        self.node = pydot.Node(self.node_name, label=self.generate_label(), shape="plaintext", dir="forward")

    def __hash__(self):
        return hash(str(tuple(map(tuple, self.board))) + str(self.g))

    def __str__(self):
        return str(self.board)

    def is_start_state(self, start_state):
        return all(self.board[i][j] == start_state[i][j] for i in range(3) for j in range(3))

    def is_goal_state(self, goal_state):
        return all(self.board[i][j] == goal_state[i][j] for i in range(3) for j in range(3))

    def generate_label(self, cell_color="grey"):

        a, b, c = self.board[0]
        d, e, f = self.board[1]
        g, h, i = self.board[2]

        cell_width = 70
        cell_blank_color = "#ffad60"
        font_size = 24

        table_cell_template = Template('<TD BGCOLOR="$cell_color" WIDTH="$cell_width" HEIGHT="$cell_width" ALIGN="center"><FONT POINT-SIZE="$font_size">$value</FONT></TD>')

        # Generate TD tag when supplied value
        generate_cell = lambda value: table_cell_template.substitute(cell_color=cell_color, cell_width=cell_width, font_size=font_size, value=value)

        label = '<'\
                '<TABLE BGCOLOR="#f57542">'\
                    '<TR>'\
                        f'<TD COLSPAN="3" WIDTH="{cell_width}" HEIGHT="{cell_width}" BGCOLOR="#f57542"><FONT POINT-SIZE="{font_size}">g={self.g}, h={self.h}, f=g + h = {self.g + self.h} </FONT></TD>'\
                    '</TR>'\
                    '<TR>'\
                        f'{generate_cell(a)}'\
                        f'{generate_cell(b)}'\
                        f'{generate_cell(c)}'\
                    '</TR>'\
                    '<TR>' \
                        f'{generate_cell(d)}' \
                        f'{generate_cell(e)}' \
                        f'{generate_cell(f)}' \
                    '</TR>' \
                    '<TR>' \
                        f'{generate_cell(g)}' \
                        f'{generate_cell(h)}' \
                        f'{generate_cell(i)}' \
                    '</TR>' \
                '</TABLE>'\
                '>'
        # Replace cell with -1 as empty cell
        label = re.sub('<TD\s+BGCOLOR=\"\w+\"\s+WIDTH=\"\d+\"\s+HEIGHT=\"\d+\"\s+ALIGN=\"\w+\"><FONT\s+POINT-SIZE=\"\d+\">\s*-1\s*</FONT></TD>',
                       f'<TD BGCOLOR="{cell_blank_color}" WIDTH="{cell_width}" HEIGHT="{cell_width}" ALIGN="center"><FONT POINT-SIZE="{font_size}"> </FONT></TD>',
                       label)

        return label