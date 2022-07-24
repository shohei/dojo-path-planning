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

print(search(G, 2, 8))
