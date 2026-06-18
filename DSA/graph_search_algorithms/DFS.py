def BFS(graph, start, goal):
    visited = []
    stack = [[start]]# we used stack here because it is BFS
    while stack:
        path = stack.pop()
        node = path[-1]
        if node in visited :
            continue
        visited.append(node)
        if node == goal:
            return path 
        else: 
            adjacent_nodes = graph.get(node, [])
            for node2 in adjacent_nodes:
                newpath = path.copy()
                newpath.append(node2)
                stack.append(newpath)

graph ={
    'S':['A','B','D'],
    'A':['C'],
    'B':['D'],
    'C':['G','D'],
    'D':['G'],
    'G':[]
}
solution = BFS(graph, 'S', 'G')
print ("solution is ",solution)               
