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
            réponse : Choisir un des deux, vu que le poids des extrémités n'a aucune importante lors de l'ordonnacement final.

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
'''

class SP_Base: 
    '''
        Constructeur de classe.
        :param source : 
        :param target : 
        :weight : poids de l'arête
    '''
    def __init__(self, source : Node = None, target : Node = None, weight = None):
        self.source = source
        self.target = target
        self.weight = weight

class SP_Serie: 
    def __init__(self, G1, G2):
        pass

class SP_parallel: 
    def __init__(self, G1, G2):
        pass

