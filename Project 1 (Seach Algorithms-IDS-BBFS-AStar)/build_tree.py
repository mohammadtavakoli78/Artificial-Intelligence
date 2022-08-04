from treelib import *
from base import *


def copy_variable(container):
    new_dic = {}
    for key in container:
        for val in container[key]:
            try:
                new_dic[key].append(val)
            except:
                new_dic[key] = [val]
    return new_dic


def build_tree(container):
    tree = Tree()
    tree.create_node("Root_Node", "Initial_Node", None, data=container)
    return tree


def expand_tree(d_tree: Tree, node: Node, play_ground):
    temp = copy_variable(node.data)
    new_ground = move(play_ground, temp, 0)

    if new_ground != -1:
        d_tree.create_node(0, d_tree.size(), node.identifier, new_ground)

    temp = copy_variable(node.data)
    new_ground = move(play_ground, temp, 1)
    if new_ground != -1:
        d_tree.create_node(1, d_tree.size(), node.identifier, new_ground)

    temp = copy_variable(node.data)
    new_ground = move(play_ground, temp, 2)
    if new_ground != -1:
        d_tree.create_node(2, d_tree.size(), node.identifier, new_ground)

    temp = copy_variable(node.data)
    new_ground = move(play_ground, temp, 3)
    if new_ground != -1:
        d_tree.create_node(3, d_tree.size(), node.identifier, new_ground)


def expand_tree2(d_tree: Tree, node: Node, play_ground):
    temp = copy_variable(node.data)
    new_ground = move2(play_ground, temp, 0)

    if new_ground != -1:
        d_tree.create_node(0, d_tree.size(), node.identifier, new_ground)

    temp = copy_variable(node.data)
    new_ground = move2(play_ground, temp, 1)
    # print(str(new_ground)+"--------")
    if new_ground != -1:
        d_tree.create_node(1, d_tree.size(), node.identifier, new_ground)

    temp = copy_variable(node.data)
    new_ground = move2(play_ground, temp, 2)
    if new_ground != -1:
        d_tree.create_node(2, d_tree.size(), node.identifier, new_ground)

    temp = copy_variable(node.data)
    new_ground = move2(play_ground, temp, 3)
    if new_ground != -1:
        d_tree.create_node(3, d_tree.size(), node.identifier, new_ground)


if __name__ == "__main__":
    build_tree(84)