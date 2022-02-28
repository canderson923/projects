import graph
import time
#C:\Users\Chris\Desktop\Spring 21\AI\pathfinding>py pathfinding.py
def default_heuristic(n):
    """
    Default heuristic for A*. Do not change, rename or remove!
    """
    return 0
    
def printEdgeList(myList):
    print("Neighbors are currently: ",end='')
    for i in range(len(myList)):
        print(myList[i].target.get_id(), end=', ')
    print('')
        
def printNodeList(myList):
    print("Nodes in list are currently: ",end='')
    for i in range(len(myList)):
        print(myList[i].get_id(), end=', ')
    print('')
    
def removeExpanded(neighbors,expanded ):
    startLength = len(neighbors) #list length of neighbors list
    hitCount = 0 #for offsetting i during pops
    #print("Current expanded list is: ", expanded)
    for i in range(startLength):
        #print("Current i = " , i)
        #printEdgeList(neighbors)
        if (len(neighbors) > 0):
            if (neighbors[i - hitCount].target.get_id() in expanded):
                neighbors.pop(i - hitCount)
                hitCount= hitCount + 1
    #printEdgeList(neighbors)

def bfs(start, goal):
    """
    Breadth-First search algorithm. The function is passed a start graph.Node object and a goal predicate.
    
    The start node can produce neighbors as needed, see graph.py for details.
    
    The goal is represented as a function, that is passed a node, and returns True if that node is a goal node, otherwise False. 
    
    The function should return a 4-tuple (path,distance,visited,expanded):
        - path is a sequence of graph.Edge objects that have to be traversed to reach a goal state from the start
        - distance is the sum of costs of all edges in the path 
        - visited is the total number of nodes that were added to the frontier during the execution of the algorithm 
        - expanded is the total number of nodes that were expanded, i.e. removed from the frontier to add their neighbors
    """
    #Variables and Lists
    path = [] 
    frontier = []
    ExpandedNodes = []
    dict = {}
    expanded, visited, length = 0,0,0
    goalFound = False
    
    #pre-setup
    frontier.append(start)
    visited = visited + 1
    #while frontier:
    while(not goalFound):
        ####Expand all nodes in frontier####
        currentLen = len(frontier)#get frontier length 
        for i in range(currentLen):
            next = frontier.pop(0) #pop node element off frontier
            if(next.get_id() not in ExpandedNodes):
                ExpandedNodes.append(next.get_id()) #add unique node id to expanded list
                expanded = expanded + 1
            #print(ExpandedNodes)
            neighbors = next.get_neighbors() #edge list of node object
            removeExpanded(neighbors,ExpandedNodes)
            #print("Expanded nodes are: ", ExpandedNodes)
            #printNodeList(frontier)
            for j in range(len(neighbors)):
                if(neighbors[j].target not in frontier):
                    frontier.append(neighbors[j].target)
                    dict[neighbors[j].target.get_id()]= next.get_id(),neighbors[j] #dictory in form of [node_id] -> came from ID, Edge
                    visited = visited + 1
                    if(goal(neighbors[j].target)): #exit if goal is in frontier
                        goalFound = True
                        currentKey = neighbors[j].target.get_id() #have the name/key of our goal for dictonary
            #printNodeList(frontier)

############back through dictionary to find path###############
    dictList = dict[currentKey]
    path.insert(0, dictList[1]) #insert goal edge
    length = dictList[1].cost
    while(dictList[0] != start.get_id()):
        currentKey = dictList[0] #change over key to where it came from
        dictList = dict[currentKey]
        path.insert(0,dictList[1]) #insert edge
        length = length + dictList[1].cost
    #print(path)       
    return path,length,visited,expanded
    
def dfs(start, goal):
    """
    Depth-First search algorithm. The function is passed a start graph.Node object, a heuristic function, and a goal predicate.
    
    The start node can produce neighbors as needed, see graph.py for details.
    
    The goal is represented as a function, that is passed a node, and returns True if that node is a goal node, otherwise False. 
    
    The function should return a 4-tuple (path,distance,visited,expanded):
        - path is a sequence of graph.Edge objects that have to be traversed to reach a goal state from the start
        - distance is the sum of costs of all edges in the path 
        - visited is the total number of nodes that were added to the frontier during the execution of the algorithm 
        - expanded is the total number of nodes that were expanded, i.e. removed from the frontier to add their neighbors
    """
    
    path = [] 
    frontier = []
    ExpandedNodes = []
    dict = {}
    expanded, visited, length = 0,0,0
    goalFound = False
    
    #pre-setup
    frontier.append(start)
    visited = visited + 1
    #while frontier:
    while(not goalFound):
        if (visited >= 1000):
            return [],0,visited,expanded
        ####Expand all nodes in frontier####
        currentLen = len(frontier)#get frontier length 
        
        next = frontier.pop(-1) #pop last element using stack method
        if(next.get_id() not in ExpandedNodes):
            ExpandedNodes.append(next.get_id()) #add unique node id to expanded list
            expanded = expanded + 1
            #print(ExpandedNodes)
        neighbors = next.get_neighbors() #edge list of node object
        removeExpanded(neighbors,ExpandedNodes)
            #print("Expanded nodes are: ", ExpandedNodes)
            #printNodeList(frontier)
        for j in range(len(neighbors)):
            if(neighbors[j].target not in frontier):
                frontier.append(neighbors[j].target)
                dict[neighbors[j].target.get_id()]= next.get_id(),neighbors[j] #dictory in form of [node_id] -> came from ID, Edge
                visited = visited + 1
                if(goal(neighbors[j].target)): #exit if goal is in frontier
                    goalFound = True
                    currentKey = neighbors[j].target.get_id() #have the name/key of our goal for dictonary
            #printNodeList(frontier)

############back through dictionary to find path###############
    dictList = dict[currentKey]
    path.insert(0, dictList[1]) #insert goal edge
    length = dictList[1].cost
    while(dictList[0] != start.get_id()):
        currentKey = dictList[0] #change over key to where it came from
        dictList = dict[currentKey]
        path.insert(0,dictList[1]) #insert edge
        length = length + dictList[1].cost
    #print(path)       
    return path,length,visited,expanded
    
def greedy(start, heuristic, goal):
    """
    Greedy search algorithm. The function is passed a start graph.Node object, a heuristic function, and a goal predicate.
    
    The start node can produce neighbors as needed, see graph.py for details.
    
    The heuristic is a function that takes a node as a parameter and returns an estimate for how far that node is from the goal.    
    
    The goal is also represented as a function, that is passed a node, and returns True if that node is a goal node, otherwise False. 
    
    The function should return a 4-tuple (path,distance,visited,expanded):
        - path is a sequence of graph.Edge objects that have to be traversed to reach a goal state from the start
        - distance is the sum of costs of all edges in the path 
        - visited is the total number of nodes that were added to the frontier during the execution of the algorithm 
        - expanded is the total number of nodes that were expanded, i.e. removed from the frontier to add their neighbors
    """
    path = [] 
    frontier = []
    ExpandedNodes = []
    dict = {}
    expanded, visited, length = 0,0,0
    goalFound = False
    
    #pre-setup
    frontier.append(start)
    visited = visited + 1
    #while frontier:
    while(not goalFound):
        
        ####Expand all nodes in frontier####
        #print("presorted")
        #printNodeList(frontier)
        frontier.sort(key = heuristic, reverse = False)
        #print("post-sorted")
        #printNodeList(frontier)
        next = frontier.pop(0) #pop first element of priority que
        if(next.get_id() not in ExpandedNodes):
            ExpandedNodes.append(next.get_id()) #add unique node id to expanded list
            expanded = expanded + 1
            #print(ExpandedNodes)
        neighbors = next.get_neighbors() #edge list of node object
        removeExpanded(neighbors,ExpandedNodes)
            #print("Expanded nodes are: ", ExpandedNodes)
            #printNodeList(frontier)
        for j in range(len(neighbors)):
            if(neighbors[j].target not in frontier):
                frontier.append(neighbors[j].target)
                dict[neighbors[j].target.get_id()]= next.get_id(),neighbors[j] #dictory in form of [node_id] -> came from ID, Edge
                visited = visited + 1
                if(goal(neighbors[j].target)): #exit if goal is in frontier
                    goalFound = True
                    currentKey = neighbors[j].target.get_id() #have the name/key of our goal for dictonary
            #printNodeList(frontier)

############back through dictionary to find path###############
    dictList = dict[currentKey]
    path.insert(0, dictList[1]) #insert goal edge
    length = dictList[1].cost
    while(dictList[0] != start.get_id()):
        currentKey = dictList[0] #change over key to where it came from
        dictList = dict[currentKey]
        path.insert(0,dictList[1]) #insert edge
        length = length + dictList[1].cost
    #print(path)       
    return path,length,visited,expanded
    

def astar(start, heuristic, goal):

    """
    A* search algorithm. The function is passed a start graph.Node object, a heuristic function, and a goal predicate.
    
    The start node can produce neighbors as needed, see graph.py for details.
    
    The heuristic is a function that takes a node as a parameter and returns an estimate for how far that node is from the goal.    
    
    The goal is also represented as a function, that is passed a node, and returns True if that node is a goal node, otherwise False. 
    
    The function should return a 4-tuple (path,distance,visited,expanded):
        - path is a sequence of graph.Edge objects that have to be traversed to reach a goal state from the start
        - distance is the sum of costs of all edges in the path 
        - visited is the total number of nodes that were added to the frontier during the execution of the algorithm 
        - expanded is the total number of nodes that were expanded, i.e. removed from the frontier to add their neighbors
    """
    path = [] 
    frontier = []
    ExpandedNodes = []
    dict = {}
    costDict = {}        
    def aStarKey(n):
        temp = heuristic(n)
        return costDict[n.get_id()] + temp
    expanded, visited, length = 0,0,0
    goalFound = False

    #pre-setup
    frontier.append(start)
    costDict[start.get_id()] = 0
    visited = visited + 1
    #while frontier:
    while(not(goalFound)):
        
        ####Expand all nodes in frontier####
        #print("presorted")
        #printNodeList(frontier)
        frontier.sort(key = aStarKey, reverse = False)
        #print("post-sorted")
        #printNodeList(frontier)
        next = frontier.pop(0) #pop first element of priority que
        if(next.get_id() not in ExpandedNodes):
            ExpandedNodes.append(next.get_id()) #add unique node id to expanded list
            expanded = expanded + 1
            #print(ExpandedNodes)
        neighbors = next.get_neighbors() #edge list of node object
        removeExpanded(neighbors,ExpandedNodes)
            #print("Expanded nodes are: ", ExpandedNodes)
            #printNodeList(frontier)
        for j in range(len(neighbors)):
            if(neighbors[j].target not in frontier):
                frontier.append(neighbors[j].target) #append next node
                costDict[neighbors[j].target.get_id()] = costDict[next.get_id()] + neighbors[j].cost
                dict[neighbors[j].target.get_id()]= next.get_id(),neighbors[j] #dictory in form of [node_id] -> came from ID, Edge
                visited = visited + 1
            if((neighbors[j].target in frontier) and ((costDict[next.get_id()] + neighbors[j].cost) < costDict[neighbors[j].target.get_id()])):
                #print("Updated the dictionary!!!")
                costDict[neighbors[j].target.get_id()] = costDict[next.get_id()] + neighbors[j].cost #update the cost dictionary
                dict[neighbors[j].target.get_id()] = next.get_id(),neighbors[j] #update travel dictonary
            if(goal(neighbors[j].target)): #exit if goal is in frontier
                goalFound = True
                currentKey = neighbors[j].target.get_id() #have the name/key of our goal for dictonary
            #printNodeList(frontier)

############back through dictionary to find path###############
    dictList = dict[currentKey]
    path.insert(0, dictList[1]) #insert goal edge
    length = dictList[1].cost
    #print(costDict)
    while(dictList[0] != start.get_id()):
        currentKey = dictList[0] #change over key to where it came from
        dictList = dict[currentKey]
        path.insert(0,dictList[1]) #insert edge
        length = length + dictList[1].cost
    #print(path)       
    return path,length,visited,expanded
    
def run_all(name, start, heuristic, goal):
    startT = time.perf_counter_ns()
    print("running test", name)
    print("Breadth-First Search")
    result = bfs(start, goal)
    stopT = time.perf_counter_ns()
    print("Time taken: ", ((stopT-startT)), " ns")
    print_path(result)
   
    print("\nDepth-First Search")
    startT = time.perf_counter_ns()
    result = dfs(start, goal)
    stopT = time.perf_counter_ns()
    print("Time taken: ", ((stopT-startT)), " ns")
    print_path(result)
    
    print("\nGreedy Search (default heuristic)")
    startT = time.perf_counter_ns()
    result = greedy(start, default_heuristic, goal)
    stopT = time.perf_counter_ns()
    print("Time taken: ", ((stopT-startT)), " ns")
    print_path(result)
    
    print("\nGreedy Search")
    startT = time.perf_counter_ns()
    result = greedy(start, heuristic, goal)
    stopT = time.perf_counter_ns()
    print("Time taken: ", ((stopT-startT)), " ns")
    print_path(result)
       
    print("\nA* Search (default heuristic)")
    startT = time.perf_counter_ns()
    result = astar(start, default_heuristic, goal)
    stopT = time.perf_counter_ns()
    print("Time taken: ", ((stopT-startT)), " ns")
    print_path(result)
    
    print("\nA* Search")
    startT = time.perf_counter_ns()
    result = astar(start, heuristic, goal)
    stopT = time.perf_counter_ns()
    print("Time taken: ", ((stopT-startT)), " ns")
    print_path(result)
    
    print("\n\n")

def print_path(result):
    (path,cost,visited_cnt,expanded_cnt) = result
    print("visited nodes:", visited_cnt, "expanded nodes:",expanded_cnt)
    if path:
        print("Path found with cost", cost)
        for n in path:
            print(n.name)
    else:
        print("No path found")
    print("\n")

def main():
    """
    You are free (and encouraged) to change this function to add more test cases.
    
    You are provided with three test cases:
        - pathfinding in Austria, using the map shown in class. This is a relatively small graph, but it comes with an admissible heuristic. Below astar is called using that heuristic, 
          as well as with the default heuristic (which always returns 0). If you implement A* correctly, you should see a small difference in the number of visited/expanded nodes between the two heuristics.
        - pathfinding on an infinite graph, where each node corresponds to a natural number, which is connected to its predecessor, successor and twice its value, as well as half its value, if the number is even.
          e.g. 16 is connected to 15, 17, 32, and 8. The problem given is to find a path from 1 to 2050, for example by doubling the number until 2048 is reached and then adding 1 twice. There is also a heuristic 
          provided for this problem, but it is not admissible (think about why), but it should result in a path being found almost instantaneously. On the other hand, if the default heuristic is used, the search process 
          will take a noticeable amount (a couple of seconds).
        - pathfinding on the same infinite graph, but with infinitely many goal nodes. Each node corresponding to a number greater 1000 that is congruent to 63 mod 123 is a valid goal node. As before, a non-admissible
          heuristic is provided, which greatly accelerates the search process. 
    """
    target = "Bregenz"
    def atheuristic(n):
        return graph.AustriaHeuristic[target][n.get_id()]
    def atgoal(n):
        return n.get_id() == target
        
    
    customTarget = "Hyrule Castle"
    def customAtheuristic(n):
        return graph.HyruleHeuristic[customTarget][n.get_id()]
    def customAtgoal(n):
        return n.get_id() == customTarget
    """
    myTupleList= []
    myTupleList.append(("Brez",124))
    myTupleList.append(("Hyrule",200))
    myTuple = myTupleList[0]
    print(list(zip(*myTupleList))[0])
    print(myTupleList[0][1])
    """
    run_all("Hyrule", graph.Hyrule["Deku Tree"], customAtheuristic, customAtgoal)
    run_all("Austria", graph.Austria["Eisenstadt"], atheuristic, atgoal)
    
    
    target = 2050
    def infheuristic(n):
        return abs(n.get_id() - target)
    def infgoal(n):
        return n.get_id() == target
    
    run_all("Infinite Graph (simple)", graph.InfNode(1), infheuristic, infgoal)
    

    def multiheuristic(n):
        return abs(n.get_id()%123 - 63)
    def multigoal(n):
        return n.get_id() > 1000 and n.get_id()%123 == 63
    
    run_all("Infinite Graph (multi)", graph.InfNode(1), multiheuristic, multigoal)
    

if __name__ == "__main__":
    main()