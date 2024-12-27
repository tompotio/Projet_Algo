class Node:
    
    def __init__(self,weight,label):
        self.weight = weight
        self.parent = {"node":None,"cost":0}
        self.label = label
        self.enfant = []

    def add_parent(self,node,cost):
       self.parent["node"] = node
       self.parent["cost"] = cost

       if(node.parent["node"]!=None):
           self.parent["node"].enfant.remove(self)
       else:
           self.parent["node"].enfant.append(self) 

class ArbreEntrant:

    def __init__(self,first,root = None):
        self.root = root
        self.first = first
        self.taille = None
        
    def add_root(self,node):
        self.root.append(node)

    def set_root(self,first):
        self.first = first

    def size(self):
        if(self.taille != None):
            return self.size
        
        roots = self.root.copy()
        noeuds = set()

        while roots != []:
            root = roots.pop()
            noeuds.add(root)

            if root.parent["node"] != None:
                roots.append(root.parent["node"])

        self.taille = len(noeuds)
        
        return len(noeuds)

"""
    Check if the sequence is valid
    """ 
def checkOrdonnancement(arbre : ArbreEntrant, ordonnancement : list):
   
    if len(ordonnancement) != arbre.size(): 
        print("Mauvaise taille")
        return -1 

    for i in range(len(ordonnancement)):
        for o2 in ordonnancement[i + 1:]:
            same = ordonnancement[i] == o2
            parent = ordonnancement[i] == o2.parent["node"]

            if same or parent: 
                print("Connard")
                return -1

def coutsNonUtilise( visitedNode : list, unvisitedNode : list):
    cost = 0
    
    for visNode in visitedNode:
        for unvisNode in unvisitedNode: 
            if visNode.parent["node"] == unvisNode: 
                cost += visNode.parent["cost"]

    return cost

def coutsProduit(node : Node):
    return node.parent["cost"]

"""
    Returns the highest cost
    :param arbre: a tree
    :param ordonnancement : sequence of nodes 
    :return: an int
    """ 
def coutOrdonnancement(arbre : ArbreEntrant, ordonnancement : list):
    visitedNode = []
    costs = []
    max = 0
    available = set()
    valide = checkOrdonnancement(arbre, ordonnancement)
    
    if valide == -1:
        return valide
    
    # Calcul par étape de l'algo
    while len(ordonnancement) > 0:
        o = ordonnancement.pop(0)
        unvisitedNodes = ordonnancement.copy()
        unvisitedNodes.append(o)

        # Récupère les différents coûts
        ws = o.weight
        """costUnused = coutsNonUtilise(visitedNode, unvisitedNodes)"""
        costUnused = sum([x.parent["cost"] for x in available])
        productCost = coutsProduit(o)
        available.add(o)
        for child in o.enfant :
            available.remove(child)
        # Fait l'addition
        cost = ws + costUnused + productCost

        # Modifie la valeur max atteinte
        if (cost > max):
            max = cost

        # Insert le node courant dans les nodes déjà visités
        visitedNode.append(o)

        # Ajoute le coût du node courant dans la liste
        costs.append(cost)
    return costs, max

# PROGRAMME 

a = Node(4,"a")
b = Node(3,"b")
c = Node(1,"c")
d = Node(2,"d")
e = Node(2,"e")
f = Node(8,"f")
g = Node(2,"g")
h = Node(1,"h")

a.add_parent(b,4)
b.add_parent(e,1)
c.add_parent(d,2)
d.add_parent(e,2)
e.add_parent(h,2)
f.add_parent(g,1)
g.add_parent(h,5)

tree = ArbreEntrant(h,[a,c,f])

ordonnancement = [f, a, b, c, d, e, g, h]

print(coutOrdonnancement(tree, ordonnancement))

'''     f a b
i       1 2 3 4 5 6  7 8
c(π, i) 9 9 9 5 8 8 10 8

'''