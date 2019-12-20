import pydot
import re

class State():
    def __init__(self, *, g, h, parent, board):
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.parent = parent
        self.board = board
        self.node_name = str(tuple(map(tuple, self.board))) + str(self.g)
        self.node = pydot.Node(self.node_name, label=self.generate_label(), shape="plaintext")

    def __hash__(self):
        return hash(str(tuple(map(tuple, self.board))) + str(self.g))

    def __str__(self):
        return str(self.board)
    
    def color_node(self):
        self.node.set("label", self.generate_label("gold"))
        # print(self.node.get("label"))
        self.node.set_label("ss")


    def is_start_state(self, start_state):
        return all(self.board[i][j] == start_state[i][j] for i in range(3) for j in range(3))
    
    def is_goal_state(self, goal_state):
        return all(self.board[i][j] == goal_state[i][j] for i in range(3) for j in range(3))

    def generate_label(self, cell_color="grey"):
        a, b, c = self.board[0]
        d, e, f = self.board[1]
        g, h, i = self.board[2]

        cell_width = 60
        cell_blank_color = "green"

        label = '<'\
                '<TABLE BGCOLOR="yellow">'\
                    '<TR>'\
                        f'<TD COLSPAN="3" WIDTH="{cell_width}" HEIGHT="{cell_width}"> g={g}, h={h}, f=g + h = { g + h} </TD>'\
                    '</TR>'\
                    '<TR>'\
                        f'<TD BGCOLOR="{cell_color}" WIDTH="{cell_width}" HEIGHT="{cell_width}" ALIGN="center">{a}</TD>'\
                        f'<TD BGCOLOR="{cell_color}" WIDTH="{cell_width}" HEIGHT="{cell_width}" ALIGN="center">{b}</TD>'\
                        f'<TD BGCOLOR="{cell_color}" WIDTH="{cell_width}" HEIGHT="{cell_width}" ALIGN="center">{c}</TD>'\
                    '</TR>'\
                    '<TR>'\
                        f'<TD BGCOLOR="{cell_color}" WIDTH="{cell_width}" HEIGHT="{cell_width}" ALIGN="center">{d}</TD>'\
                        f'<TD BGCOLOR="{cell_color}" WIDTH="{cell_width}" HEIGHT="{cell_width}" ALIGN="center">{e}</TD>'\
                        f'<TD BGCOLOR="{cell_color}" WIDTH="{cell_width}" HEIGHT="{cell_width}" ALIGN="center">{f}</TD>'\
                    '</TR>'\
                    '<TR>'\
                        f'<TD BGCOLOR="{cell_color}" WIDTH="{cell_width}" HEIGHT="{cell_width}" ALIGN="center">{g}</TD>'\
                        f'<TD BGCOLOR="{cell_color}" WIDTH="{cell_width}" HEIGHT="{cell_width}" ALIGN="center">{h}</TD>'\
                        f'<TD BGCOLOR="{cell_color}" WIDTH="{cell_width}" HEIGHT="{cell_width}" ALIGN="center">{i}</TD>'\
                    '</TR> '\
                '</TABLE>'\
                '>'
        label = re.sub('<TD\s+BGCOLOR=\"\w*\"\s+WIDTH=\"\d*\"\s+HEIGHT=\"\d*\"\s+ALIGN=\"\w*\">\s*-1\s*</TD>', f'<TD BGCOLOR="{cell_blank_color}" WIDTH="{cell_width}" HEIGHT="{cell_width}" ALIGN="center"> </TD>', label)
        return label
        # return "{ {"+str(a)+"|"+str(b)+"|"+ str(c) +"}"+"|{"+str(d)+"|"+str(e)+"|"+str(f)+"}| {"+str(g)+"|"+str(h)+"|"+str(i)+"}}"


