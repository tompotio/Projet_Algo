from forkjoin import *

'''
    Observations : 
        + Dans l'exemple "composition", il n'y a aucune différence entre t1 et s2. ✅
            Il faut imaginer que la Composition de G1 et G2 est une série parallèle qui s'est concaténée unifiant t1 et s2.

        + J'ai l'impression que pour crée un graphe en série parallèle, il faut toujours donner un s et un t. C'est également le cas de base. ❌

    Réflexions : 
        + Pour la composition en série entre G1 et G2 : 
            - Est-ce que s1 c'est le s de G1 ou un s en plus ?
            réponse : le s1 est directement celui de G1

            - De la même façon est-ce que le t2 est le t de G2 ?
            réponse : le t2 est directement celui de t2

        + Quels poids choisir lors de la fusion des sommets ? Par exemple lors d'une composition en série.
            réponse : Choisir un des deux, vu que le poids des extrémités n'a aucune importante lors de l'ordonnancement final.

        + Lors d'une composition parallèle de deux séries parallèle basique, quelles fusions sont possibles ? 
            réponse :
                Avant fusion :         Après fusion :
                s1 -> t1               s -> t
                s2 -> t2

            (En gros l'idée c'est que l'on perd les sommets en de nouveaux sommets, donc on s'en fiche des labels précédents)

    Brainstorming : 

        Constructeur de graphe en série parallèle ✅
            SP(s : terminaisonNode, t : terminaisonNode) : Crée un graphe série parallèle (j'ai pas mis toutes les infos, c'est une juste une rep à l'arrache)

        Fonction qui renvoie une composition en série de G1 et G2 (une série parallèle) ❌
            serie(G1 : SP, G2 : SP) : 

        Fonction qui renvoie une composition en parallèle de G1 et G2 ❌
            parallele(G1 : SP, G2 : SP)


        Mieux vaut faire un constructeur qui se charge des trois cas. ❌

        Pour le calcul de l'ordonnancement des sous-graphe : 
            1. S'il s'agit d'un cas de base ou en série, il suffit de retourner la liste du parcours des sommets du graphe.
            2. S'il s'agit d'une série en parallèle, il faut d'abord faire l'étape 1, ensuite linéairiser en créant des chaînes. Puis on calcule l'ordonnancement optimal du fork join associé.
            3. On continue récursivement s'il y a des imbrications de merde.

        Etape quand je retourne l'ordonnancement du forkjoin

        1. Je crée mes chaînes (linéarisation)
        2. Je crée mon forkJoin
        3. Je récupère l'ordonnancement
        4. Je modifie les noeuds de terminaison par des noeuds normaux
        5. Je retourne l'ordonnancement modifié

'''

class SPGraph:
    '''
        Classe abstraite de base pour un graphe Série Parallèle.
        :param source : Noeud source.
        :param target : Noeud cible.
    '''
    def __init__(self, source =  None, target = None, label = ""):
        self.source = source
        self.target = target
        self.label = label

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

    def getType(self):
        return ""

class SP_Base(SPGraph):
    '''
        Constructeur pour le case de base.
        :param source : Noeud source.
        :param target : Noeud cible.
        :param weight : Poids de l'arête.
    '''
    def __init__(self, source = None, target = None, weight = None):
        super().__init__(source, target)
        self.weight = weight

    def ordonnancement(self): 
        return [self.source, self.target]

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
        G1.target = fusedNode
        G2.source = fusedNode

        # On plug le nouveau node
        fusedNode.parent = G2.source.parent
        fusedNode.enfant[0] = G1.source.enfant[0]

        self.G1 = G1
        self.G2 = G2

    def ordonnancement(self):
        G1_Ordo = G1.ordonnancement()
        G2_Ordo = G2.ordonnancement()

        # On retire le premier élément de G2_Ordo qui est commun avec G1_Ordo (dernier élément de celui-ci)
        G2_Ordo_sans_premier = G2_Ordo[1:]

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
        # Crée une nouvelle source et une nouvelle cible
        
        # On fusionne s1 et s2
        fusedSources = self.fuseNode(G1.src, G2.src)

        # On fusionne t1 et t2
        fusedTarget = self.fuseNode(G1.target, G2.target)

        '''
        Je traiterai les cas de base avec n'importe quoi après...
        # Si G1 et G2 sont des cas de base
        if G1.getType() == G2.getType(): 
            src1_cost = G1.src.parent["cost"]  
            src2_cost = G2.src.parent["cost"]
            fusedSources.parent["cost"] = src1_cost + src2_cost
        '''

        # Si 
        if G1.getType() != "SP_Base" and G2.getType() != "SP_Base" : 
            fusedSources.parent = 

        super().__init__(fusedSources, fusedTarget)

        # Liste des sous-graphes.
        self.G1 = G1
        self.G2 = G2

    def ordonnancement(self):
        pass

    def getType(self):
        return "SP_Parallel"

'''
    Transforme le graphe en chaîne en respectant l'ordonnancement optimal passé en paramètre.
'''
def lineariser(graphe : SP, ordonnancement : list):
    return

'''
    Prend en entrée un graphe série parallèle et retourne un ordonnancement minimisant le coût d'exécution
'''
def ordonnancementSerieParallele(graphe : SP)
    return graphe.ordonnancement()
