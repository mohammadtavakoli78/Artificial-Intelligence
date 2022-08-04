from base import *
from IDS import *
from BBFS import *
from A import *
from gui import *

play_ground, container = get_options()

# goal, d_tree = IDS(play_ground, container, 12)
# a = get_path(goal, d_tree)
# print(a[0])
# print(a[1])
# print(a[1])

d_tree, r_tree, d, node = BBFS(play_ground, container)
a = get_path(d, d_tree)
b = get_path(node, r_tree)
print(a[0])
# print(b[0][::-1])
print(a[1])
print(a[1])

# goal, d_tree = A(play_ground, container)
# a = get_path(goal, d_tree)
# cost = get_g(goal, d_tree)
# print(a[0])
# print(a[1])
# print(cost)

path = a[0].split(" ")
finalPath = []
for d in path:
    if d == "U":
        finalPath.append(0)
    elif d == "R":
        finalPath.append(1)
    elif d == "D":
        finalPath.append(2)
    elif d == "L":
        finalPath.append(3)

visualize = Visualize(play_ground, container, finalPath)
visualize.render()
