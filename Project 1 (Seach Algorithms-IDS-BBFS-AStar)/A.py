from build_tree import *


def get_g(node: Node, d_tree: Tree):
    temp = 0
    if node.data['g']:
        temp += node.data['g'][0]
    a = d_tree.parent(node.identifier)
    while a:
        if a and a.tag != 'Root_Node':
            temp += a.data['g'][0]
            a = d_tree.parent(a.identifier)
        else:
            break
    return temp


def A(play_ground, container):
    d_tree = build_tree(container)
    list = [d_tree.get_node(d_tree.root)]

    explored = []

    while list:

        node = list.pop()
        flag = True

        state = copy_variable(node.data)

        try:
            del state['g']
            del state['distance']
        except:
            pass
        for d in explored:
            if d == state:
                flag = False
        if flag:
            expand_tree(d_tree, node, play_ground)

            state = copy_variable(node.data)
            try:
                del state['g']
                del state['distance']
            except:
                pass
            explored.append(state)

            heuristic = []

            children = d_tree.children(node.identifier)

            for c in children:
                c.data['distance'] = [c.data['distance'][0] + get_g(c, d_tree)]

            list += children
            list = sorted(list, key=lambda x: x.data['distance'], reverse=True)

            if node.data['finish'][0]:
                return node, d_tree

    print("can't pass the butter")
    exit(0)