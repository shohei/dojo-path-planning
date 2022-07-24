target_locations = {'r': 1, 'g': 5, 'b': 7, 'y': 3} 
target_carry_path = {'r': ['lower-left'], 'g': ['upper-left'], 
                     'b': ['upper-left'], 'y': ['right','lower-right'] }
class Edge():
    def __init__(self, to, w):
        self.to = to
        self.w = w

G = [[Edge(1,1),Edge(3,1)],
     [Edge(0,1),Edge(2,1),Edge(4,1)],
     [Edge(5,1),Edge(1,1)],
     [Edge(0,1),Edge(4,1),Edge(6,1)],
     [Edge(1,1),Edge(3,1),Edge(5,1),Edge(7,1)],
     [Edge(2,1),Edge(4,1),Edge(8,1)],
     [Edge(3,1),Edge(7,1)],
     [Edge(4,1),Edge(6,1),Edge(8,1)],
     [Edge(5,1),Edge(7,1)]]

def search(G,s,e):
    INF = 9999
    N = len(G)
    prev_nodes = [-1]*N

    used = [False]*N
    dist = [INF]*N
    dist[s] = 0
    prev_nodes[s]=-1
    for _ in range(N):
        min_dist = INF
        min_v = -1
        for v in range(N):
            if used[v]==False and dist[v] < min_dist:
                min_dist = dist[v]
                min_v = v

        if min_v==-1:
            break

        for edge in G[min_v]:
            if dist[edge.to] > dist[min_v]+edge.w:
                dist[edge.to] = dist[min_v]+edge.w
                prev_nodes[edge.to] = min_v

        used[min_v] = True

    prev_node = e
    path = []
    while prev_node!=-1:
        path.append(prev_node)
        prev_node = prev_nodes[prev_node]
    path.reverse()
    return path
# print(search(G, 2, 8))

connections = {0: {1:'right',  3:'left'},
               1: {2:'right',  4: 'down', 0: 'left'},
               2: {5: 'down',  1: 'left'},
               3: {4: 'right', 6: 'down', 0: 'up'},
               4: {5: 'right', 7: 'down', 1: 'up', 3: 'left'},
               5: {2: 'up',    4: 'left', 8: 'down'},
               6: {7: 'right', 3: 'up'},
               7: {8: 'right', 4: 'up', 6: 'left'}}

command_table = {'up': {'up': 'F', 'upper-right': 'R45F', 'right': 'R90F',
                        'lower-right': 'R135F', 'down': 'R180F', 'lower-left': 'L135F',
                         'left': 'L90F', 'upper-left': 'L45F'},
                 'upper-right':  {'up': 'L45F', 'upper-right': 'F', 'right': 'R45F',
                        'lower-right': 'R90F', 'down': 'R135F', 'lower-left': 'R180F',
                         'left': 'L135F', 'upper-left': 'L90F'},
                 'right':  {'up': 'L90F', 'upper-right': 'L45F', 'right': 'F',
                        'lower-right': 'R45F', 'down': 'R90F', 'lower-left': 'R135F',
                         'left': 'R180F', 'upper-left': 'L135F'},
                 'lower-right':  {'up': 'L135F', 'upper-right': 'L90F', 'right': 'L45F',
                        'lower-right': 'F', 'down': 'R45F', 'lower-left': 'R90F',
                         'left': 'R135F', 'upper-left': 'R180F'},
                 'down':  {'up': 'R180F', 'upper-right': 'L135F', 'right': 'L90F',
                        'lower-right': 'L45F', 'down': 'F', 'lower-left': 'R45F',
                         'left': 'R90F', 'upper-left': 'R135F'},
                 'lower-left':  {'up': 'R135F', 'upper-right': 'R180F', 'right': 'L135F',
                        'lower-right': 'L90F', 'down': 'L45F', 'lower-left': 'F',
                         'left': 'R45F', 'upper-left': 'R90F'},
                 'left':  {'up': 'R90F', 'upper-right': 'R135F', 'right': 'R180F',
                        'lower-right': 'L135F', 'down': 'L90F', 'lower-left': 'L45F',
                         'left': 'F', 'upper-left': 'R45F'},
                 'upper-left':  {'up': 'R45F', 'upper-right': 'R90F', 'right': 'R135F',
                        'lower-right': 'R180F', 'down': 'L135F', 'lower-left': 'L90F',
                         'left': 'L45F', 'upper-left': 'F'}}

multiple_backward_table = {
    'right': {'upper-right': ['B','R45B'], 'lower-right': ['B','L45B']},
    'left': {'upper-left': ['B','L45B'], 'lower-left': ['B','R45B']},
    'down': {'lower-left': ['B','L45B'], 'lower-right': ['B','R45B']},
    'up': {'upper-right': ['B','L45B'], 'upper-right': ['B','R45B']}
}

def generate_backward_path(forward_path):
    if len(forward_path)==1:
        return 'B'
    if len(forward_path)==2:
        return multiple_backward_table[forward_path[0]][forward_path[1]]

if __name__=="__main__":
    work_order = ['r','g','b','y']
    init_pos = 0
    init_direction = 'down'
    path = [init_pos]
    for w in work_order:
        current = path.pop()
        destination = target_locations[w]
        shortest_path = search(G, current, destination)
        for i in range(len(shortest_path)-1):
            direction = connections[shortest_path[i]][shortest_path[i+1]]
            path.append(direction)
        forward_path = target_carry_path[w]
        path.append('Pick')
        path.extend(forward_path)
        path.append('Release')
        backward_path = generate_backward_path(forward_path)
        path.extend(backward_path)
        path.append(target_locations[w])

    current = path.pop()
    destination = init_pos 
    shortest_path = search(G, current, destination)
    for i in range(len(shortest_path)-1):
        direction = connections[shortest_path[i]][shortest_path[i+1]]
        path.append(direction)

    print(path)

    direction_array = ['up','down','right','left',  
                       'upper-left','upper-right','lower-left','lower-right']

    current = init_direction 
    INIT_VAL = 0
    next = INIT_VAL 
    commands = []
    while True:
        while next not in direction_array: 
            if next != INIT_VAL:
                commands.append(next) 
            next = path.pop(0)
        # print(current, next)
        command = command_table[current][next]
        commands.append(command)
        if len(path)==0:
            break
        current = next
        next = path.pop(0)

    print(commands)