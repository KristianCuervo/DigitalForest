import numpy as np
from numpy import eye, array, zeros
from math import cos, sin, pi

def rotation_matrix(angle, axis):
    R = eye(4, dtype=float)
    i1, i2 = (axis + 1) % 3, (axis + 2) % 3
    R[i1, i1] = cos(angle)
    R[i1, i2] = -sin(angle)
    R[i2, i1] = sin(angle)
    R[i2, i2] = cos(angle)
    return R

def translation_matrix(v):
    T = eye(4, dtype=float)
    T[0:3, 3] = v
    return T

class SpaceTurtle:
    """
    - forward(d): move d units UP along +Y
    - turn(a):   yaw about Y
    - roll(a):   roll about Z
    - push/pop:  stack state
    - set_width(w): thickness
    """
    def __init__(self, init_width):
        self.T = eye(4, dtype=float)
        self.w = init_width
        self.stack = []

    def push(self):
        self.stack.append((self.T.copy(), self.w))

    def pop(self):
        self.T, self.w = self.stack.pop()

    def set_width(self, w):
        self.w = w

    def forward(self, d):
        # Now moves along Y axis! (vertical growth)
        self.T = self.T @ translation_matrix(array([0.0, d, 0.0], dtype=float))

    def turn(self, a):
        # yaw around Y
        self.T = self.T @ rotation_matrix(a, axis=1)

    def roll(self, a):
        # roll around Z
        self.T = self.T @ rotation_matrix(a, axis=0)

    def get_pos(self):
        p = self.T @ array([0.0, 0.0, 0.0, 1.0], dtype=float)
        return p[:3]

def realize(symbols):
    """
    Converts an L-system symbol list into:
      verts  : (N×3) array of 3D points
      edges  : list of (child_idx, parent_idx)
      radii  : (N,) array of segment widths
    """
    turtle = SpaceTurtle(init_width=symbols[0][1])
    verts   = [turtle.get_pos()]
    edges   = []
    radii   = {0: turtle.w}
    v_idx   = 0
    stack   = []

    for sym in symbols:
        cmd = sym[0]
        if cmd == 'F':
            d = sym[1]
            turtle.forward(d)
            parent = v_idx
            v_idx = len(verts)
            verts.append(turtle.get_pos())
            edges.append((v_idx, parent))
            radii[v_idx] = turtle.w

        elif cmd == '+':
            turtle.turn(sym[1]*pi/180)
        elif cmd == '-':
            turtle.turn(-sym[1]*pi/180)
        elif cmd == '/':
            turtle.roll(sym[1]*pi/180)
        elif cmd == '!':
            turtle.set_width(sym[1])
        elif cmd == '[':
            turtle.push(); stack.append(v_idx)
        elif cmd == ']':
            turtle.pop(); v_idx = stack.pop()
        # ignore any other symbols

    verts = np.array(verts, dtype=float)
    R     = zeros(len(verts), dtype=float)
    for idx, w in radii.items():
        R[idx] = w

    #print("Inside turtle")
    #print(R)
    print(verts)
    return verts, edges, R
