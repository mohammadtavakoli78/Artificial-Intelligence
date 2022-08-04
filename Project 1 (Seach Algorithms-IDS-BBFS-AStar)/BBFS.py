from build_tree import *
from base import *


def BBFS(play_ground, container):
    # print(container)
    container2 = check_goal(copy_variable(container), play_ground)
    # print(container2)
    d_tree = build_tree(container)
    r_tree = build_tree(container2)

    list = [d_tree.get_node(d_tree.root)]
    list2 = [r_tree.get_node(r_tree.root)]

    explored = []
    explored2 = []

    while list:
        node = list[0]
        del list[0]

        flag = True

        for d in explored:
            if d.data == node.data:
                flag = False
        if flag:
            expand_tree(d_tree, node, play_ground)
            list += d_tree.children(node.identifier)
            # print(node)
            explored.append(node)
            if node.data['finish'][0]:
                return d_tree, d_tree, node, node

        if not list2:
            continue

        node = list2[0]
        del list2[0]

        if node.data in explored2:
            pass
        else:
            for d in explored:
                if d.data == node.data:
                    return d_tree, r_tree, d, node
            expand_tree2(r_tree, node, play_ground)
            list2 += r_tree.children(node.identifier)
            explored2.append(node.data)
            # print(str(node)+",84")

    print("can't pass the butter")
    exit(0)