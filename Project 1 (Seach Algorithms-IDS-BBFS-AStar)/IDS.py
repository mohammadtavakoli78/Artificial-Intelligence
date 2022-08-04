from build_tree import *


def get_path(goal: Node, d_tree: Tree):
    depth = d_tree.depth(goal.identifier)
    list = []
    path = ''
    list.append(goal.tag)
    a = d_tree.parent(goal.identifier)
    list.append(a.tag)
    while a:
        a = d_tree.parent(a.identifier)
        if a and a.tag != 'Root_Node':
            list.append(a.tag)
    for i in list:
        if i == 0:
            path += 'U '
        elif i == 1:
            path += 'R '
        elif i == 2:
            path += 'D '
        elif i == 3:
            path += 'L '
    path = path[::-1]
    return path, depth


def IDS(play_ground, container, cutoff):
    for i in range(10, cutoff):
        d_tree = build_tree(container)
        list = [d_tree.get_node(d_tree.root)]

        while list:
            node = list.pop()
            if d_tree.depth(node) >= i:
                continue
            expand_tree(d_tree, node, play_ground)
            for child in d_tree.children(node.identifier):
                list.append(child)
                # print(child)
                if child.data['finish'][0]:
                    return child, d_tree
    print("can't pass the butter")
    exit(0)
