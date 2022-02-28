

class Node:
    def get_id(self):
        """
        Returns a unique identifier for the node (for example, the name, the hash value of the contents, etc.), used to compare two nodes for equality.
        """
        return ""
    def get_neighbors(self):
        """
        Returns all neighbors of a node, and how to reach them. The result is a list Edge objects, each of which contains 3 attributes: target, cost and name, 
        where target is a Node object, cost is a numeric value representing the distance between the two nodes, and name is a string representing the path taken to the neighbor.
        """
        return []
    def __eq__(self, other):
        return self.get_id() == other.get_id()
        
class Edge:
    """
    Abstraction of a graph edge. Has a target (Node that the edge leads to), a cost (numeric) and a name (string), which can be used to print the edge.
    """
    def __init__(self, target, cost, name):
        self.target = target 
        self.cost = cost
        self.name = name

class GeomNode(Node):
    """
    Representation of a finite graph in which all nodes are kept in memory at all times, and stored in the node's neighbors field.
    """
    def __init__(self, name):
        self.name = name
        self.neighbors = []
    def get_neighbors(self):
        return self.neighbors
    def get_id(self):
        return self.name
        
class InfNode(Node):
    """
    Infinite graph, in which every node represents an integer, and neighbors are generated on demand. Note that Nodes are not cached, i.e. if you
    request the neighbors of node 1, and the neighbors of node 3, both will contain the node 2, but they will be using two distinct objects. 
    """
    def __init__(self, nr):
        self.nr = nr
    def get_neighbors(self):
        result = [Edge(InfNode(self.nr-1),1,("%d - -1 - %d"%(self.nr,self.nr-1))), Edge(InfNode(self.nr+1),1,("%d - +1 - %d"%(self.nr,self.nr+1))), Edge(InfNode(self.nr*2),1,("%d - *2 - %d"%(self.nr,self.nr*2)))]
        if self.nr%2 == 0:
            result.append(Edge(InfNode(self.nr//2),1,("%d - /2 - %d"%(self.nr,self.nr//2))))
        return result
    def get_id(self):
        return self.nr


def make_geom_graph(nodes, edges):
    """
    Given a list of nodes and edges (with distances), creates a dictionary of Node objects 
    representing the graph. Note that the resulting graph is directed, but each edge will be 
    replaced with *two* directed edges (to and from).
    """
    result = {}
    for c in nodes:
        result[c] = GeomNode(c)
    for (a,b,d) in edges:
        result[a].neighbors.append(Edge(result[b], d, "%s - %s"%(a,b)))
        result[b].neighbors.append(Edge(result[a], d, "%s - %s"%(b,a)))
    return result
    
Austria = make_geom_graph(
    ["Graz", "Vienna", "Salzburg", "Innsbruck", "Munich", "Bregenz", "Linz", "Eisenstadt", "Klagenfurt", "Lienz", "Bruck"],
    [("Graz", "Bruck", 55.0),
     ("Graz", "Klagenfurt", 136.0),
     ("Graz", "Vienna", 200.0),
     ("Graz", "Eisenstadt", 173.0),
     ("Bruck", "Klagenfurt", 152.0),
     ("Bruck", "Salzburg", 215.0),
     ("Bruck", "Linz", 195.0),
     ("Bruck", "Vienna", 150.0),
     ("Vienna", "Eisenstadt", 60.0),
     ("Vienna", "Linz", 184.0),
     ("Linz", "Salzburg", 123.0),
     ("Salzburg", "Munich", 145.0),
     ("Salzburg", "Klagenfurt", 223.0),
     ("Klagenfurt", "Lienz", 145.0),
     ("Lienz", "Innsbruck", 180.0),
     ("Munich", "Innsbruck", 151.0),
     ("Munich", "Bregenz", 180.0),
     ("Innsbruck", "Bregenz", 190.0)])
     
     
#Greedy path-> Graz -> Klagenfurt -> Salzburg ->Munich -> Bregenz
AustriaHeuristic = { 
   "Graz":       {"Graz": 0.0,   "Vienna": 180.0, "Eisenstadt": 150.0, "Bruck": 50.0,  "Linz": 225.0, "Salzburg": 250.0, "Klagenfurt": 125.0, "Lienz": 270.0, "Innsbruck": 435.0, "Munich": 375.0, "Bregenz": 450.0},
   "Vienna":     {"Graz": 180.0, "Vienna": 0.0,   "Eisenstadt": 50.0,  "Bruck": 126.0, "Linz": 175.0, "Salzburg": 285.0, "Klagenfurt": 295.0, "Lienz": 400.0, "Innsbruck": 525.0, "Munich": 407.0, "Bregenz": 593.0},
   "Eisenstadt": {"Graz": 150.0, "Vienna": 50.0,  "Eisenstadt": 0.0,   "Bruck": 171.0, "Linz": 221.0, "Salzburg": 328.0, "Klagenfurt": 335.0, "Lienz": 437.0, "Innsbruck": 569.0, "Munich": 446.0, "Bregenz": 630.0},
   "Bruck":      {"Graz": 50.0,  "Vienna": 126.0, "Eisenstadt": 171.0, "Bruck": 0.0,   "Linz": 175.0, "Salzburg": 201.0, "Klagenfurt": 146.0, "Lienz": 287.0, "Innsbruck": 479.0, "Munich": 339.0, "Bregenz": 521.0},
   "Linz":       {"Graz": 225.0, "Vienna": 175.0, "Eisenstadt": 221.0, "Bruck": 175.0, "Linz": 0.0,   "Salzburg": 117.0, "Klagenfurt": 311.0, "Lienz": 443.0, "Innsbruck": 378.0, "Munich": 265.0, "Bregenz": 456.0},
   "Salzburg":   {"Graz": 250.0, "Vienna": 285.0, "Eisenstadt": 328.0, "Bruck": 201.0, "Linz": 117.0, "Salzburg": 0.0,   "Klagenfurt": 201.0, "Lienz": 321.0, "Innsbruck": 265.0, "Munich": 132.0, "Bregenz": 301.0},
   "Klagenfurt": {"Graz": 125.0, "Vienna": 295.0, "Eisenstadt": 335.0, "Bruck": 146.0, "Linz": 311.0, "Salzburg": 201.0, "Klagenfurt": 0.0,   "Lienz": 132.0, "Innsbruck": 301.0, "Munich": 443.0, "Bregenz": 465.0},
   "Lienz":      {"Graz": 270.0, "Vienna": 400.0, "Eisenstadt": 437.0, "Bruck": 287.0, "Linz": 443.0, "Salzburg": 321.0, "Klagenfurt": 132.0, "Lienz": 0.0,   "Innsbruck": 157.0, "Munich": 298.0, "Bregenz": 332.0},
   "Innsbruck":  {"Graz": 435.0, "Vienna": 525.0, "Eisenstadt": 569.0, "Bruck": 479.0, "Linz": 378.0, "Salzburg": 265.0, "Klagenfurt": 301.0, "Lienz": 157.0, "Innsbruck": 0.0,   "Munich": 143.0, "Bregenz": 187.0},
   "Munich":     {"Graz": 375.0, "Vienna": 407.0, "Eisenstadt": 446.0, "Bruck": 339.0, "Linz": 265.0, "Salzburg": 132.0, "Klagenfurt": 443.0, "Lienz": 298.0, "Innsbruck": 143.0, "Munich": 0.0,   "Bregenz": 165.0},
   "Bregenz":    {"Graz": 450.0, "Vienna": 593.0, "Eisenstadt": 630.0, "Bruck": 521.0, "Linz": 456.0, "Salzburg": 301.0, "Klagenfurt": 465.0, "Lienz": 332.0, "Innsbruck": 187.0, "Munich": 165.0, "Bregenz": 0.0}}

Hyrule = make_geom_graph(
    ["Deku Tree","Deku Entrance","Kokiri Forest Center","Kokiri to Hyrule Field","Hyrule Field to Kokiri","Lost Woods","Forest Temple",	"Lon Lon","Hyrule Field to Zora River","Zora River mid way","Zora Domain",
    "Hyrule Field to Kakariko",	"Kakariko Mid",	"Kakariko cem ent",	"Shadow Temple","Kakariko DM ent",	"Gorgon City",	"Fire Temple",	"Hyrule City ent",	"Hyrule City center",	"Temple of Light",
    "Hyrule city to castle","Hyrule Castle","Gerudo Valley","Haunted Wastelands","Desert Colossus",	"Spirit Temple",	"Lake Hylia",	"Water Temple"],
    [("Deku Tree","Deku Entrance", 51.0),
     ("Deku Entrance", "Kokiri Forest Center", 82.5),
     ("Kokiri Forest Center","Kokiri to Hyrule Field" , 120.4),
     ("Kokiri Forest Center","Lost Woods" , 131.53),
     ("Lost Woods","Forest Temple" , 234.0),
     ("Kokiri to Hyrule Field","Hyrule Field to Kokiri" , 36.0),
     ("Hyrule Field to Kokiri","Lon Lon" , 139.0),
     ("Hyrule Field to Kokiri","Hyrule Field to Zora River" , 72.0),
     ("Hyrule Field to Kokiri", "Hyrule Field to Kakariko", 141.0),
     ("Hyrule Field to Kokiri","Hyrule City ent" , 153.0),
     ("Hyrule Field to Kokiri","Gerudo Valley" , 370.0),
     ("Hyrule Field to Kokiri","Lake Hylia" , 192.0),
     ("Hyrule City ent","Hyrule Field to Zora River" , 117.0),
     ("Hyrule City ent","Lon Lon" , 94.0),
     ("Hyrule City ent","Hyrule Field to Kakariko" , 61.0),
     ("Hyrule City ent", "Hyrule City center", 45.0),
     ("Hyrule City ent","Temple of Light" , 72.0),
     ("Hyrule City ent","Gerudo Valley" , 314.0),
     ("Hyrule Field to Kakariko","Lon Lon" , 142.0),
     ("Hyrule Field to Kakariko","Hyrule Field to Zora River", 81.0),
     ("Hyrule Field to Kakariko","Kakariko Mid" , 71.0),
     ("Hyrule Field to Zora River","Lon Lon" , 151.0),
     ("Hyrule Field to Zora River","Zora River mid way" , 72.0),
     ("Zora River mid way","Zora Domain" , 121.0),
     ("Lon Lon","Lake Hylia", 145.0),
     ("Lon Lon","Gerudo Valley", 243.0),
     ("Lake Hylia","Water Temple", 113.0),
     ("Lake Hylia","Gerudo Valley", 223.0),
     ("Gerudo Valley","Haunted Wastelands" , 58.0),
     ("Haunted Wastelands","Desert Colossus" , 120.0),
     ("Desert Colossus", "Spirit Temple", 90.0),
     ("Hyrule City center", "Temple of Light", 38.0),
     ("Hyrule City center", "Hyrule city to castle", 35.0),
     ("Hyrule city to castle", "Hyrule Castle", 41.0),
     ("Temple of Light", "Hyrule city to castle", 36.0),
     ("Kakariko Mid","Kakariko cem ent" , 36.0),
     ("Kakariko Mid","Kakariko DM ent" , 36.0),
     ("Kakariko cem ent","Shadow Temple", 57.0),
     ("Kakariko Mid","Gorgon City" , 91.0),
     ("Gorgon City","Fire Temple", 92.0)])
HyruleHeuristic = { 
    "Hyrule Castle":{"Deku Tree":376.0,"Deku Entrance":346.0,"Kokiri Forest Center":415.0,"Kokiri to Hyrule Field":297.0,"Hyrule Field to Kokiri":262.0,"Lost Woods":300.0,"Forest Temple":332.0,"Lon Lon":206.0,"Hyrule Field to Zora River":206.0,
    "Zora River mid way":184.0,"Zora Domain":260.0,"Hyrule Field to Kakariko":125.0,"Kakariko Mid":126.0,"Kakariko cem ent":145.0,"Shadow Temple":180.0,"Kakariko DM ent":94.0,	"Gorgon City":116.0,"Fire Temple":192.0,
    "Hyrule City ent":120.0,"Hyrule City center":75.0,	"Temple of Light":72.0,"Hyrule city to castle":41.0,"Hyrule Castle":0.0,"Gerudo Valley":376.0,"Haunted Wastelands":428.0,"Desert Colossus":488.0,
    "Spirit Temple":560.0,"Lake Hylia":352.0,"Water Temple":458.0}}
