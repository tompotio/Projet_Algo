import math

# =====================================================
#                      STRUCTURES
# =====================================================

class Node:
    def __init__(self,weight,label):
        self.weight = weight
        self.parent = {"node" : None,"cost" : 0}
        self.label = label
        self.enfant = []

    def add_parent(self,node,cost):
       if self.parent["node"] != None:
           self.parent["node"].enfant.remove(self)
       self.parent["node"] = node
       self.parent["cost"] = cost
       self.parent["node"].enfant.append(self) 

class ArbreEntrant:
    def __init__(self, first, root = []):
        self.root = root
        self.first = first
        self.taille = None

    def size(self):
        
        if(self.taille != None):
            return self.taille

        
        enfants = self.first.enfant.copy()
       
        taille = 1
        
        while enfants != []:
            enfant = enfants.pop()
            enfants.extend(enfant.enfant)
            taille += 1

        self.taille = taille
        
        return taille


# =====================================================
#                   CALCUL DES COUTS
# =====================================================

"""
    Check if the sequence is valid
    """ 
def checkOrdonnancement(arbre : ArbreEntrant, ordonnancement : list):
    
    if len(ordonnancement) != arbre.size():
        print("incomplet")
        return -1 

    for i in range(len(ordonnancement)):
        for o2 in ordonnancement[i + 1:]:
            same = ordonnancement[i] == o2
            parent = False
            
            if (o2.parent["node"] != None):
                parent = ordonnancement[i] == o2.parent["node"]

            if same or parent:
                print("incorrect")
                return -1

"""
    Returns the highest cost
    :param arbre: a tree
    :param ordonnancement : sequence of nodes 
    :return: an int
""" 
def coutOrdonnancement(arbre : ArbreEntrant, ordonnancement : list):
    max = 0
    costs = []
    segment = []
    available = set()
    
    valide = checkOrdonnancement(arbre, ordonnancement)
    
    if valide == -1:
        return valide
    
    # Calcul par étape de l'algo
    while len(ordonnancement) > 0:
        o = ordonnancement.pop(0)

        # Récupère les différents coûts
        ws = o.weight
        costUnused = sum([x.parent["cost"] for x in available])
        productCost = o.parent["cost"]
        
        # Insert le node courant dans les nodes avec encore des liens
        available.add(o)

        for child in o.enfant :
            available.remove(child)
        
        # Fait l'addition
        cost = ws + costUnused + productCost

        # Modifie la valeur max atteinte
        if (cost > max):
            max = cost

        # Ajoute le coût du node courant dans la liste
        costs.append(cost)

    return max

def segment(arbre : ArbreEntrant, ordonnancement: list):
    costs = []
    segment = []
    available = set()
    valide = checkOrdonnancement(arbre, ordonnancement)
    coutExecution = 0
    if valide == -1:
        return valide
    
    # Calcul par étape de l'algo
    while len(ordonnancement) > 0:
        o = ordonnancement.pop(0)
        # Récupère les différents coûts
        ws = o.weight
        costUnused = sum([x.parent["cost"] for x in available])
        productCost = o.parent["cost"]
        
        available.add(o)
        for child in o.enfant :
            available.remove(child)

        coutResiduel = sum([x.parent["cost"] for x in available])
        # Fait l'addition
        cost = ws + costUnused + productCost
        coutExecution = max(cost,coutExecution)
        # Ajoute le coût du node courant dans la liste
        costs.append({"node" : o, "cost" : cost, "residual" : coutResiduel})

    # Initialise le premier segment
    segment.append({"node" : [], "h" : -math.inf, "v" : math.inf})

    # Ajout des segments
    for cost in range(len(costs) - 1):
        segment[len(segment) - 1]["node"].append(costs[cost]["node"])
        
        if costs[cost]["residual"] < segment[len(segment) - 1]["v"] :
            segment[len(segment) - 1]["v"] = costs[cost]["residual"]
            
        if costs[cost]["cost"] > segment[len(segment) - 1]["h"] :
            segment[len(segment) - 1]["h"] = costs[cost]["cost"]

        if costs[cost]["cost"] == coutExecution and costs[cost + 1]["cost"] != coutExecution :
            segment.append({"node" : [], "h" : -math.inf, "v" : math.inf})
    
    # Ajout du dernier segment
    segment[len(segment) - 1]["h"] = max(costs[len(costs) - 1]["cost"], segment[len(segment) - 1]["h"])
    segment[len(segment) - 1]["v"] = min(costs[len(costs) - 1]["residual"], segment[len(segment) - 1]["v"])
    segment[len(segment) - 1]["node"].append(costs[len(costs) - 1]["node"])

    return segment

def ordonnancementArbre(arbre: ArbreEntrant):
    node = arbre.first
    
    # Si on tombe sur une feuille, retourne juste le noeud
    if not node.enfant:
        return [node]

    res = []
    segments = []

    # On calcule les ordonnancements pour chaque enfant
    for enfant in node.enfant:
        sousArbre = ArbreEntrant(enfant)

        # Calcule l'ordonnancement optimal pour cet enfant 
        ordonnancement_enfants = ordonnancementArbre(sousArbre)

        # Calcule les segments pour cet ordonnancement
        segmentsEnfant = segment(sousArbre, ordonnancement_enfants)

        # Stocke tous les segments avec leurs informations
        segments.extend(segmentsEnfant)

    # Trie globalement les segments pour tous les enfants
    segments.sort(key=lambda seg: seg["h"] - seg["v"], reverse=True)

    # Ajoute les noeuds des segments dans l'ordre optimal
    for seg in segments:
        res.extend(seg["node"])

    # Ajoute la racine à la fin de l'ordonnancement
    res.append(node)

    return res

