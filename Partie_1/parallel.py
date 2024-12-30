from forkjoin import *

'''
    Classe abstraite de base pour un graphe Série Parallèle.
'''
class SPGraph:
    '''
        Constructeur pour les séries parallèle.
        :param source : Poids du noeud source OU un noeud source.
        :param target : Poids du noud target OU un noeud target.
        :param edge_weight : Poids de l'arête entre les deux nœuds (facultatif).
    '''
    def __init__(self, source, target, edge_weight = None):
        if edge_weight is not None:
            self.source = terminaisonNode(source, "s")
            self.target = terminaisonNode(target, "t") 
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
    '''
    def fuseNode(self, node1, node2, label = ""):
        # Somme des noeuds
        somme = node1.weight + node2.weight

        # Renommage (par défaut concatène les labels des noeuds)
        newLabel = ""
        if len(label) > 0: 
            newLabel = label
        else: 
            newLabel = node1.label + "/" + node2.label
        
        # Génère le nouveau noeud
        fusionNode = Node(somme, newLabel)

        return fusionNode

    def plugSource(self, newSource, parents):
        for parent in parents:
            parent.enfant[0] = newSource

    def plugTarget(self, newTarget, enfants):
        for enfant in enfants: 
            enfant.parent["node"] = newTarget

    def getType(self):
        return ""

class SP_Base(SPGraph):
    '''
        Constructeur pour le case de base.
        :param source : Noeud source.
        :param target : Noeud cible.
        :param weight : Poids de l'arête.
    '''
    def __init__(self, sourceWeight, targetWeight, edge_weight):
        super().__init__(sourceWeight, targetWeight, edge_weight)

    def ordonnancement(self):
        return []

    def getType(self):
        return "SP_Base"

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
        fusedNode.parent = G1.target.parent
        fusedNode.enfant = G2.source.enfant

        # On plug les parents de la source de G2 au nouveau noeud
        self.plugSource(fusedNode, G2.source.parent)

        # On plug les enfants de la target de G1 au nouveau noeud
        self.plugTarget(fusedNode, G1.target.enfant)

        G1.target = fusedNode
        G2.source = fusedNode

        self.G1 = G1
        self.G2 = G2

    def ordonnancement(self):
        G1_Ordo = self.G1.ordonnancement()
        G2_Ordo = self.G2.ordonnancement()

        # On retire le premier élément de G2_Ordo qui est commun avec G1_Ordo (dernier élément de celui-ci)
        G2_Ordo_sans_premier = G2_Ordo[1:]
        
        G2_Ordo_sans_premier.append(self.target)

        # Concatène les deux listes
        return G1_Ordo + G2_Ordo_sans_premier

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