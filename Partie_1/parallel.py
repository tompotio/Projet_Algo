from forkjoin import *

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
        srcLabel = srcLabel if srcLabel else "s"
        targetLabel = targetLabel if targetLabel else "t"

        # S'il y a le poids de l'arête. Et que source et target sont également des poids, alors on est en train de définir un case de base.
        if (edge_weight is not None) and (isinstance(source, int)) and (isinstance(target, int)):
            self.source = terminaisonNode(source, srcLabel)
            self.target = terminaisonNode(target, targetLabel)
            self.edge_weight = edge_weight
        else:
            self.source = source
            self.target = target

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
        fusionNode = Node(somme, newLabel)

        return fusionNode

    def plugSource(self, newSource, parents):
        for parent in parents:
            parent.enfant[0] = newSource

    def plugTarget(self, newTarget, enfants):
        for enfant in enfants: 
            enfant.parent[0] = newTarget

    def getType(self):
        return ""

    def print_SP(self):
        for parent in self.source.parent: 
            current = self.source
            output = "Affiche SP : [" + current.label

            while current != self.target:
                current = current.parent[0]
                output += "," + current.label

            output += "]"
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
    def __init__(self, G1, G2):
        super().__init__(G1.source, G2.target)

        # On fusionne t1 à s2
        fusedNode = self.fuseNode(G1.target, G2.source)

        # On plug le nouveau node avec les anciens parents et enfants
        fusedNode.enfant = G1.target.enfant
        fusedNode.parent = G2.source.parent

        # On plug les parents de la source de G2 au nouveau noeud
        self.plugSource(fusedNode, G2.source.parent)

        # On plug les enfants de la target de G1 au nouveau noeud
        self.plugTarget(fusedNode, G1.target.enfant)

        G1.target = fusedNode
        G2.source = fusedNode

        self.G1 = G1
        self.G2 = G2

    def ordonnancement(self):
        PremierMembre = [self.source]
        SecondMembre = [self.G2.source]

        # On récupère l'ordonnancement de G1 et on lui retire le premier et le denier élément
        G1_Ordo = self.G1.ordonnancement()
        G1_Ordo = G1_Ordo[1:-1]

        # On récupère l'ordo de G2 et on lui ajoute le self.target
        G2_Ordo = self.G2.ordonnancement()
        G2_Ordo = G2_Ordo[:-1] # On retire le dernier élément de G2_Ordo par défaut
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
    def __init__(self, G1, G2):        
        # On fusionne s1 et s2
        fusedSources = self.fuseNode(G1.source, G2.source)

        # On fusionne t1 et t2
        fusedTarget = self.fuseNode(G1.target, G2.target)

        # On plug nos nouveaux noeuds avec les anciens enfants et parents
        fusedSources.parent = G1.source.parent
        fusedSources.parent.extend(G2.source.parent)
        fusedTarget.enfant = G1.target.enfant
        fusedSources.enfant.extend(G2.target.enfant)

        # On le fait également pour les enfants et les parents dans l'autre sens (liste doublement chaînée)
        self.plugSource(fusedSources, G1.target.parent)
        self.plugSource(fusedSources, G2.target.parent)
        self.plugTarget(fusedSources, G1.source.enfant)
        self.plugTarget(fusedSources, G2.source.enfant)

        # Si on est sur une composition en parallèle de deux case de base, on fusionne également l'arête
        if (G1.getType() == "SP_Base" and G2.getType() == "SP_Base"):
            G1_edge_weight = G1.edge_weight
            G2_edge_weight = G2.edge_weight
            fusedSources.edge_weight = G1_edge_weight + G2_edge_weight

        super().__init__(fusedSources, fusedTarget)

        # Liste des sous-graphes.
        self.G1 = G1
        self.G2 = G2

    def ordonnancement(self):
        fork_join = forkJoin(self.source.weight, self.target.weight)

        # On récupère les ordonnancements de nos sous-graphes
        G1_ordo = self.G1.ordonnancement()
        G2_ordo = self.G2.ordonnancement()

        # On construit les chaînes de nos sous-graphes
        G1_chaine = lineariser(self.G1, G1_ordo)
        G2_chaine = lineariser(self.G2, G2_ordo)

        # Ajout les chaînes respectives à notre forkJoin
        fork_join.add_chain(G1_chaine, self.G1.edge_weight)
        fork_join.add_chain(G2_chaine, self.G2.edge_weight)

        # Renvoie l'ordonnancement optimal
        return fork_join.ordonnancementForkJoin()

    def getType(self):
        return "SP_Parallel"

'''
    Transforme le graphe en chaîne en respectant l'ordonnancement optimal passé en paramètre.
'''
def lineariser(graphe : SPGraph, ordonnancement : list) :
    chaine = []

    # Rajoute à la chaîne chaque node dans l'ordre de l'ordonnancement
    for node in ordonnancement:
        chaine.append(node)

    # Restera plus qu'à adapter les pondérations

    return chaine

'''
    Prend en entrée un graphe série parallèle et retourne un ordonnancement minimisant le coût d'exécution
'''
def ordonnancementSerieParallele(graphe : SPGraph):
    return graphe.ordonnancement()

# Tests pour Série parallèle

# Création des bases
base1 = SP_Base(1,1,"a","b",1)
base2 = SP_Base(1,1,"c","d",1)
base3 = SP_Base(1,1,"a1","b1",1)
base4 = SP_Base(1,1,"c1","d1",1)

# Composition en série
serie = SP_Serie(base1, base2)
serie2 = SP_Serie(base3, base4)
serie3 = SP_Serie(serie, serie2)

ordonnancement = serie3.ordonnancement()

#ordonnancement = serie3.ordonnancement()
print("Ordonnancement optimal :", [node.label for node in ordonnancement])