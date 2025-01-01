from forkjoin import *

class WeightRegistry:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WeightRegistry, cls).__new__(cls, *args, **kwargs)
            cls._instance.weights = {}
        return cls._instance

    def set_weight(self, node1, node2, weight):
        key = tuple(sorted((node1, node2), key=lambda x: x.label))
        self.weights[key] = weight

    def get_weight(self, node1, node2):
        key = tuple(sorted((node1, node2), key=lambda x: x.label))
        return self.weights.get(key, None)

    def remove_weight(self, node1, node2):
        key = tuple(sorted((node1, node2), key=lambda x: x.label))
        self.weights.pop(key, None)

    def list_weights(self):
        return self.weights

'''
    Classe abstraite de base pour un graphe Série Parallèle.
'''
class SPGraph:
    '''
        Constructeur pour les séries parallèle.
        Le constructeur gère deux cas. Les classes définies de manière récursive (en parallèle et en série) ou bien la classe de base.

        :param source : Poids du noeud source OU un noeud source.
        :param target : Poids du noud target OU un noeud target.
        :param srcLabel : Nom du label source.
        :param targetLabel : Nom du label target.
        :param edge_weight : Poids de l'arête entre les deux nœuds (facultatif).
    '''
    def __init__(self, source, target, srcLabel="", targetLabel="", edge_weight=None):
        self.registry = WeightRegistry()

        srcLabel = srcLabel if srcLabel else "s"
        targetLabel = targetLabel if targetLabel else "t"

        # S'il y a le poids de l'arête. Et que source et target sont également des poids, alors on est en train de définir un case de base.
        if (edge_weight is not None) and (isinstance(source, int)) and (isinstance(target, int)):
            self.source = terminaisonNode(source, srcLabel)
            self.target = terminaisonNode(target, targetLabel)
            self.set_edge_weight(self.source, self.target, edge_weight)
        else:
            self.source = source
            self.target = target

    def set_edge_weight(self, node1, node2, weight):
        self.registry.set_weight(node1, node2, weight)

    def get_edge_weight(self, node1, node2):
        return self.registry.get_weight(node1, node2)
    
    def remove_edge_weight(self, node1, node2):
        self.registry.remove_weight(node1, node2)

    '''
        Définition de la fonction de calcul du meilleur ordonnancement à override dans chaque classe.
    '''
    def ordonnancement(self): 
        pass

    '''
        Fusionne deux noeuds en faisant l'addition de leurs poids
        Optionnellement on peut donner un nom au nouveau noeud (par défaut le nom est égal à la concaténation des labels des noeuds précédents)
    '''
    def fuseNode(self, node1, node2, label = ""):
        # Somme des noeuds
        somme = node1.weight + node2.weight

        # Renommage (par défaut concatène les labels des noeuds)
        newLabel = ""
        if len(label) > 0: 
            newLabel = label
        else: 
            print("Fusionne : ", node1.label, " avec ", node2.label)
            newLabel = node1.label + "/" + node2.label
        
        # Génère le nouveau noeud
        fusionNode = terminaisonNode(somme, newLabel)

        return fusionNode

    '''
        Plug les parents de l'ancien noeud au nouveau
    ''' 
    def plugSource(self, newSource, oldSource, parents):
        for parent in parents:
            oldWeight = self.get_edge_weight(oldSource, parent)
            parent.enfant.append(newSource)
            parent.enfant.remove(oldSource)
            self.set_edge_weight(newSource, parent, oldWeight)
            self.remove_edge_weight(oldSource, parent)

    '''
        Plug les enfants de l'ancien noeud au nouveau
    ''' 
    def plugTarget(self, newTarget, oldTarget, enfants):
        for enfant in enfants: 
            oldWeight = self.get_edge_weight(enfant, oldTarget)
            enfant.parent.append(newTarget)
            enfant.parent.remove(oldTarget)
            self.set_edge_weight(enfant, newTarget, oldWeight)
            self.remove_edge_weight(enfant, oldTarget)
            
    def getType(self):
        return ""

    '''
        Affiche le graphe avec les poids des sommets. 
        A noter donc, que l'affichage ne prend pas en compte les poids des arêtes.
    '''
    def print_SP(self):
        output = "Affiche " + self.getType() +  " : \n"

        for parent in self.source.parent: 
            current = self.source
            output += "  [" + current.label + "(" + str(current.weight) + ")"
            last = current
            current = parent

            while current != self.target:
                output += " -{" + str(self.get_edge_weight(last, current)) + "}-> " + current.label + "(" + str(current.weight) + ")"
                
                last = current
                current = current.parent[0]

            output += " -{" + str(self.get_edge_weight(last, current)) + "}-> " + current.label + "(" + str(current.weight) + ")]\n" 

        print(output)

class SP_Base(SPGraph):
    '''
        Constructeur pour le case de base.
        :param source : Noeud source.
        :param target : Noeud cible.
        :param weight : Poids de l'arête.
    '''
    def __init__(self, sourceWeight, targetWeight, srcLabel, targetLabel, edge_weight):
        super().__init__(sourceWeight, targetWeight, srcLabel, targetLabel, edge_weight)

        self.source.parent = [self.target]
        self.target.enfant = [self.source]

    def ordonnancement(self):
        return []

    def getType(self):
        return "SP_Base"

    def print_SP(self):
        print("[", self.source.label, ",", self.target.label, "]")

class SP_Serie(SPGraph):
    '''
        Constructeur pour une composition en série.
        :param G1 : Premier sous-graphe.
        :param G2 : Deuxième sous-graphe.
    '''
    def __init__(self, G1, G2, fusedLabel):
        super().__init__(G1.source, G2.target)

        # On fusionne t1 à s2
        fusedNode = self.fuseNode(G1.target, G2.source, fusedLabel)

        # On plug le nouveau node avec les anciens parents et enfants
        fusedNode.enfant = G1.target.enfant
        fusedNode.parent = G2.source.parent

        # On plug les parents de la source de G2 au nouveau noeud
        self.plugSource(fusedNode, G2.source, G2.source.parent)

        # On plug les enfants de la target de G1 au nouveau noeud
        self.plugTarget(fusedNode, G1.target, G1.target.enfant)

        G1.target = fusedNode
        G2.source = fusedNode

        self.G1 = G1
        self.G2 = G2

    def ordonnancement(self):
        PremierMembre = [self.source]
        SecondMembre = [self.G2.source]

        # On récupère l'ordonnancement de G1 et on lui retire le premier et le dernier élément
        G1_Ordo = self.G1.ordonnancement()
        G1_Ordo = G1_Ordo[1:-1]

        # On récupère l'ordo de G2 et on lui ajoute le self.target
        G2_Ordo = self.G2.ordonnancement()
        G2_Ordo = G2_Ordo[1:-1] # On retire le dernier élément de G2_Ordo par défaut

        G2_Ordo.append(self.target)

        # Renvoie la concaténation du tout
        return PremierMembre + G1_Ordo + SecondMembre + G2_Ordo 

    def getType(self):
        return "SP_Serie"

class SP_Parallel(SPGraph):
    '''
        Constructeur pour une composition en parallèle.
        :param G1 : Premier sous-graphe.
        :param G2 : Deuxième sous-graphe.
    '''
    def __init__(self, G1, G2, fusedSourcesLabel = "", fusedTargetLabel = ""):        
        # On fusionne les sources
        fusedSources = self.fuseNode(G1.source, G2.source, fusedSourcesLabel)

        # On fusionne les cibles
        fusedTarget = self.fuseNode(G1.target, G2.target, fusedTargetLabel)

        super().__init__(fusedSources, fusedTarget)

        # On inscrit les parents des sources au nouveau noeud
        fusedSources.parent = G1.source.parent + G2.source.parent

        # On inscrit les enfants des cibles au nouveau noeud
        fusedTarget.enfant = G1.target.enfant + G2.target.enfant

        # On le fait également pour les enfants et les parents dans l'autre sens (liste doublement chaînée)
        self.plugSource(fusedSources, G1.source, G1.source.parent)
        self.plugSource(fusedSources, G2.source, G2.source.parent)
        self.plugTarget(fusedTarget, G1.target, G1.target.enfant)
        self.plugTarget(fusedTarget, G2.target, G2.target.enfant)

        # Si on est sur une composition en parallèle de deux case de base, on fusionne également l'arête
        if (G1.getType() == "SP_Base" and G2.getType() == "SP_Base"):
            G1_edge_weight = G1.edge_weight
            G2_edge_weight = G2.edge_weight
            self.set_edge_weight(fusedSources, fusedTarget, (G1_edge_weight + G2_edge_weight))

        G1.source = fusedSources
        G2.source = fusedSources
        G1.target = fusedTarget
        G2.target = fusedTarget

        # Liste des sous-graphes.
        self.G1 = G1
        self.G2 = G2

    def ordonnancement(self):
        fork_join = forkJoin(self.source.weight, self.target.weight)

        # On récupère les ordonnancements de nos sous-graphes
        G1_ordo = self.G1.ordonnancement()
        G2_ordo = self.G2.ordonnancement()

        # On construit les chaînes de nos sous-graphes
        G1_chaine = lineariser(self.G1, G1_ordo[1:-1])
        G2_chaine = lineariser(self.G2, G2_ordo[1:-1])

        # Ajoute les chaînes respectives à notre forkJoin 
        # (On peut récupérer "cost" car on est sûr qu'après la linéarisation les noeuds de la chaîne ne sont pas des terminaisons)
        fork_join.add_chain(G1_chaine, G1_chaine[0].parent["cost"])
        fork_join.add_chain(G2_chaine, G2_chaine[0].parent["cost"])

        # Renvoie l'ordonnancement optimal
        return fork_join.ordonnancementForkJoin()

    def getType(self):
        return "SP_Parallel"

'''
    Transforme le graphe en chaîne en respectant l'ordonnancement optimal passé en paramètre.
'''
def lineariser(graphe : SPGraph, ordonnancement : list):

    chaine = []

    # Rajoute à la chaîne chaque node dans l'ordre de l'ordonnancement
    for i in range(0, len(ordonnancement) - 1):
        current = ordonnancement[i]

        if current.parent[0] != ordonnancement[i + 1]:
            pass

    # Restera plus qu'à adapter les pondérations

    return chaine

'''
    Prend en entrée un graphe série parallèle et retourne un ordonnancement minimisant le coût d'exécution
'''
def ordonnancementSerieParallele(graphe : SPGraph):
    return graphe.ordonnancement()

# Tests pour Série parallèle

'''
# Exemple 1
# Création des bases
base1 = SP_Base(1,1,"a","b",1)
base2 = SP_Base(1,1,"c","d",1)
base3 = SP_Base(1,1,"a1","b1",1)
base4 = SP_Base(1,1,"c1","d1",1)

# Composition en série
serie = SP_Serie(base1, base2)
serie2 = SP_Serie(base3, base4)
serie3 = SP_Serie(serie, serie2)

ordonnancement = serie2.ordonnancement()

#ordonnancement = serie3.ordonnancement()
print("Ordonnancement optimal :", [node.label for node in ordonnancement])
'''

'''
Ordonnancement optimal pour l'exemple qui suit quand il s'agit d'un forkJoin :
    ['s', 'c2_1', 'c1_1', 'c2_2', 'c3_1', 'c3_2', 'c2_3', 'c1_2', 'c1_3', 'c3_3', 't']

(On doit normalement trouver la même chose avec nos SP)
'''

# Création de la première chaîne
base1 = SP_Base(1,2,"s","x",4)
base2 = SP_Base(1,3,"x'","y",1)
serie1 = SP_Serie(base1,base2,"c1_1")

base3 = SP_Base(1,3,"x'", "y'",2)
serie2 = SP_Serie(serie1,base3,"c1_2")

base4 = SP_Base(2,8,"x'","t",3)
chaine1 = SP_Serie(serie2, base4, "c1_3")

#chaine1.print_SP()

# Création de la seconde chaîne
base5 = SP_Base(1,3,"s","x",3)
base6 = SP_Base(1,6,"x'","y",4)
serie4 = SP_Serie(base5,base6,"c2_1")

base7 = SP_Base(1,5,"x'", "y'",1)
serie5 = SP_Serie(serie4,base7,"c2_2")

base8 = SP_Base(3,0,"x'","t",1)
chaine2 = SP_Serie(serie5, base8, "c2_3")

#chaine2.print_SP()

# Création de la troisième chaîne
base9 = SP_Base(0,11,"s","x",4)
base10 = SP_Base(1,10,"x'","y",5)
serie7 = SP_Serie(base9,base10,"c3_1")

base11 = SP_Base(1,0,"x'", "y'",6)
serie8 = SP_Serie(serie7,base11,"c3_2")

base12 = SP_Base(1,0,"x'","t",6)
chaine3 = SP_Serie(serie8, base12, "c3_3")

ordonnancement = chaine3.ordonnancement()

#chaine3.print_SP()

# Création du Sp en parallèle associé

para1 = SP_Parallel(chaine1, chaine2, "s", "t")

para2 = SP_Parallel(para1, chaine3, "s", "t")
para2.print_SP()

print([str(weight) for weight in chaine3.registry.list_weights().values()])