import os
import enum


class robotAction(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def check_goal(container, play_ground):
    robot = container['robot']
    butters = container['butters']
    obstacle = container['obstacle']
    destination = container['destination']
    row = len(play_ground)
    column = len(play_ground[0])

    butters = destination.copy()

    dest_row = destination[0][0]
    dest_column = destination[0][1]

    if dest_row > 1 and (dest_row - 2, dest_column) not in obstacle and (dest_row - 1, dest_column) not in obstacle:
        robot = [(dest_row - 1, dest_column)]
    elif dest_column < column - 2 and (dest_row, dest_column + 2) not in obstacle and (dest_row, dest_column + 2) not in obstacle:
        robot = [(dest_row, dest_column + 1)]
    elif dest_row < row - 2 and (dest_row + 2, dest_column) not in obstacle and (dest_row + 1, dest_column) not in obstacle:
        robot = [(dest_row + 1, dest_column)]
    elif dest_column > 1 and (dest_row, dest_column - 2) not in obstacle and (dest_row, dest_column - 1) not in obstacle:
        robot = [(dest_row, dest_column - 1)]

    container['robot'] = robot
    container['butters'] = butters
    return container


def move(play_ground, container, action):
    tempRobot = container['robot'][0]
    robot = container['robot']
    butters = container['butters']
    obstacle = container['obstacle']
    destination = container['destination']
    distance = 1000000
    distance2 = 1000000
    butterIndex = 0

    row = len(play_ground)
    column = len(play_ground[0])

    if action == robotAction.UP.value:
        if robot[0][0] != 0 and not ((robot[0][0]-1, robot[0][1]) in obstacle) and not ((robot[0][0]-1, robot[0][1]) in destination):
            if (robot[0][0]-1, robot[0][1]) in butters and robot[0][0]-1 > 0 and (robot[0][0]-2, robot[0][1]) not in obstacle:
                index = butters.index((robot[0][0]-1, robot[0][1]))
                butters[index] = (butters[index][0] - 1, butters[index][1])
                robot[0] = (robot[0][0] - 1, robot[0][1])
            elif not ((robot[0][0]-1, robot[0][1]) in butters):
                robot[0] = (robot[0][0] - 1, robot[0][1])
    elif action == robotAction.RIGHT.value:
        if robot[0][1] != column - 1 and not ((robot[0][0], robot[0][1]+1) in obstacle) and not ((robot[0][0], robot[0][1]+1) in destination):
            if (robot[0][0], robot[0][1]+1) in butters and robot[0][1]+1 != column - 1 and (robot[0][0], robot[0][1]+2) not in obstacle:
                index = butters.index((robot[0][0], robot[0][1]+1))
                butters[index] = (butters[index][0], butters[index][1]+1)
                robot[0] = (robot[0][0], robot[0][1] + 1)
            elif not ((robot[0][0], robot[0][1] + 1) in butters):
                robot[0] = (robot[0][0], robot[0][1] + 1)
    elif action == robotAction.DOWN.value:
        if robot[0][0] != row - 1 and not ((robot[0][0]+1, robot[0][1]) in obstacle) and not ((robot[0][0]+1, robot[0][1]) in destination):
            if (robot[0][0]+1, robot[0][1]) in butters and robot[0][0]+1 != row - 1 and (robot[0][0]+2, robot[0][1]) not in obstacle:
                index = butters.index((robot[0][0]+1, robot[0][1]))
                butters[index] = (butters[index][0] + 1, butters[index][1])
                robot[0] = (robot[0][0] + 1, robot[0][1])
            elif not ((robot[0][0] + 1, robot[0][1]) in butters):
                robot[0] = (robot[0][0] + 1, robot[0][1])
    elif action == robotAction.LEFT.value:
        if robot[0][1] != 0 and not ((robot[0][0], robot[0][1]-1) in obstacle) and not ((robot[0][0], robot[0][1]-1) in destination):
            if (robot[0][0], robot[0][1] - 1) in butters and robot[0][1]-1 != 0 and (robot[0][0], robot[0][1]-2) not in obstacle:
                index = butters.index((robot[0][0], robot[0][1]-1))
                butters[index] = (butters[index][0], butters[index][1] - 1)
                robot[0] = (robot[0][0], robot[0][1] - 1)
            elif not((robot[0][0], robot[0][1] - 1) in butters):
                robot[0] = (robot[0][0], robot[0][1] - 1)

    container['robot'] = robot
    container['butters'] = butters

    counter = 0
    for b in butters:
        if abs(robot[0][0] - b[0]) + abs(robot[0][1] - b[1]) < distance:
            distance2 = abs(robot[0][0] - b[0]) + abs(robot[0][1] - b[1])
            butterIndex = counter
            counter += 1

    for d in destination:
        if abs(butters[butterIndex][0] - d[0]) + abs(butters[butterIndex][1] - d[1]) < distance:
            distance = abs(butters[butterIndex][0] - d[0]) + abs(butters[butterIndex][1] - d[1])

    distance += distance2

    container['g'] = [int(play_ground[robot[0][0]][robot[0][1]][0])]
    container['distance'] = [distance]

    flag = True
    for i in butters:
        if i not in destination:
            flag = False
    if flag:
        container['finish'] = [True]
        return container
    elif robot[0] == tempRobot:
        return -1
    else:
        return container


def move2(play_ground, container, action):
    tempRobot = container['robot'][0]
    robot = container['robot']
    butters = container['butters']
    obstacle = container['obstacle']
    destination = container['destination']

    row = len(play_ground)
    column = len(play_ground[0])

    if action == robotAction.UP.value:
        if robot[0][0] != row - 1 and not ((robot[0][0]+1, robot[0][1]) in obstacle):
            if (robot[0][0]-1, robot[0][1]) in butters:
                index = butters.index((robot[0][0]-1, robot[0][1]))
                butters[index] = (butters[index][0] + 1, butters[index][1])
                robot[0] = (robot[0][0] + 1, robot[0][1])
            elif not ((robot[0][0] - 1, robot[0][1]) in butters):
                robot[0] = (robot[0][0] + 1, robot[0][1])
    elif action == robotAction.RIGHT.value:
        if robot[0][1] != 0 and not ((robot[0][0], robot[0][1]-1) in obstacle):
            if (robot[0][0], robot[0][1] + 1) in butters:
                index = butters.index((robot[0][0], robot[0][1]+1))
                butters[index] = (butters[index][0], butters[index][1] - 1)
                robot[0] = (robot[0][0], robot[0][1] - 1)
            elif not((robot[0][0], robot[0][1] + 1) in butters):
                robot[0] = (robot[0][0], robot[0][1] - 1)
    elif action == robotAction.DOWN.value:
        if robot[0][0] != 0 and not ((robot[0][0] - 1, robot[0][1]) in obstacle):
            if (robot[0][0] + 1, robot[0][1]) in butters:
                index = butters.index((robot[0][0] + 1, robot[0][1]))
                butters[index] = (butters[index][0] - 1, butters[index][1])
                robot[0] = (robot[0][0] - 1, robot[0][1])
            elif not ((robot[0][0] + 1, robot[0][1]) in butters):
                robot[0] = (robot[0][0] - 1, robot[0][1])
    elif action == robotAction.LEFT.value:
        if robot[0][1] != column - 1 and not ((robot[0][0], robot[0][1]+1) in obstacle):
            if (robot[0][0], robot[0][1] - 1) in butters:
                index = butters.index((robot[0][0], robot[0][1]-1))
                butters[index] = (butters[index][0], butters[index][1] + 1)
                robot[0] = (robot[0][0], robot[0][1] + 1)
            elif not((robot[0][0], robot[0][1] - 1) in butters):
                robot[0] = (robot[0][0], robot[0][1] + 1)

    container['robot'] = robot
    container['butters'] = butters

    flag = True
    for i in butters:
        if i not in destination:
            flag = False
    if flag:
        container['finish'] = [True]

    if robot[0] == tempRobot or robot[0] in butters or container['finish'][0]:
        return -1
    else:
        return container


def find_neighbors(tuple, x, y):
    print('-------')
    print(tuple)
    print('-------')
    neighbors = []
    neighbors.extend(
        [
            (tuple[0] + 1, tuple[1]) if tuple[0] + 1 <= x else None,
            (tuple[0], tuple[1] + 1) if tuple[1] + 1 <= y else None,
            (tuple[0] - 1, tuple[1]) if tuple[0] - 1 >= 0 else None,
            (tuple[0], tuple[1] - 1) if tuple[1] - 1 >= 0 else None
        ]
    )
    return neighbors


def read_file(file):
    f = open(os.path.join(os.path.dirname(__file__), file), mode='r')
    play_ground = []
    for i in f.readlines()[1:]: play_ground.append(i.split('\t'))
    for i in range(len(play_ground) - 1): play_ground[i][-1] = play_ground[i][-1].replace('\n', '')
    return play_ground


def get_options():
    play_ground = read_file('input/test1.txt')
    width = len(play_ground)
    lenght = len(play_ground[0])

    robot = []
    destination = []
    butters = []
    obstacle = []
    g = []
    distance = []

    visited = []
    queue = []

    container = {}

    for y, val in enumerate(play_ground):
        for x, j in enumerate(val):
            robot.append(tuple((y, x))) if 'r' in j else None
            destination.append(tuple((y, x))) if 'p' in j else None
            butters.append(tuple((y, x))) if 'b' in j else None
            obstacle.append(tuple((y, x))) if 'x' in j else None

    container['robot'] = robot
    container['destination'] = destination
    container['butters'] = butters
    container['obstacle'] = obstacle
    container['finish'] = [False]
    container['g'] = g
    container['distance'] = distance

    if not container['obstacle']:
        container['obstacle'] = [(-1, -1)]
    return play_ground, container


if __name__ == "__main__":
    play_ground = read_file('input/test2.txt')
    width = len(play_ground)
    lenght = len(play_ground[0])

    robot = []
    destination = []
    butters = []
    obstacle = []

    visited = []
    queue = []

    container = {}

    for y, val in enumerate(play_ground): 
        for x, j in enumerate(val):
            robot.append(tuple((y, x))) if 'r' in j else None
            destination.append(tuple((y, x))) if 'p' in j else None
            butters.append(tuple((y, x))) if 'b' in j else None
            obstacle.append(tuple((y, x))) if 'x' in j else None

    container['robot'] = robot
    container['destination'] = destination
    container['butters'] = butters
    container['obstacle'] = obstacle

    container2 = move2(play_ground=play_ground, container={'robot': [(3,4)], 'destination': [(3,3)], 'butters': [(3,3)], 'obstacle': [0,0]}, action=3)
    print(container2)

