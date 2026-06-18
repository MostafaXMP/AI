graph ={
    'S': [('A', 2), ('D', 5), ('B', 3)],
    'A': [('C', 4)],
    'B': [('D', 4)],
    'C': [('G', 2), ('D', 1)],
    'D': [('G', 5)],
    'G': []  
}

def path_cost(path):
    total_cost = 0
    for node, cost in path:
        total_cost += cost
    return total_cost

def UCS(graph, start, goal):
    visited = []
    queue = [[(start, 0)]]#here we will input the start point and its cost
    while queue:
        queue.sort(key=path_cost)#to make it a priority queue we must sort the queue according to the least cost  
        path = queue.pop(0)#pop the first element which has the least cost
        node = path[-1][0]#-1 to  get the element in the right(last element which contains (S,cost=0) ) then get S from the path to check if it is visited or not
        if node in visited:
            continue
        visited.append(node)
        if node == goal:
            return path
        else:
            adjacent_nodes = graph.get(node, []) 
            for node2, cost in adjacent_nodes:
                newpath = path.copy()
                newpath.append((node2, cost))
                queue.append(newpath)


solution = UCS(graph, 'S', 'G')
print("Solution path:", solution)
print("Cost of solution:", path_cost(solution))