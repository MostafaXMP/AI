def BFS(graph, start, goal):
    visited = []# we put in it the visited nodes
    queue = [[start]]#we use a queue to impelement the UCS and input the start point
    while queue:#this means that the loop goes while the queue not empty
        path = queue.pop(0)#pop the first element *so it is removed from the queue* and make it inside the path
        node = path[-1]#-1 to  get the element in the right from the path to check if it is visited or not
        if node in visited :
            continue
        visited.append(node)
        if node == goal:#it checks if the node is the goal or not if yes it will return the path
            return path # the while loop stops when it find the goal and correct the path
        else: 
            adjacent_nodes = graph.get(node, [])# this gets the adjecent of the node [A,D,B] ; the adjecent is now [A,D,B]
            for node2 in adjacent_nodes:#this makes the node2 be equal to each element in the list of adjecent (node2 = 'A')
                newpath = path.copy()# path = 's' so the new path = 's' #this is constant for all the loop
                newpath.append(node2)# add to the new path node2 which is 'A' so the newpath will be = ['S','A'] #newpath will be = ['S','B']
                queue.append(newpath)# queue is increased to be like the path ['S','A']#queue will be = [['S','A'],['S','B']]

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
