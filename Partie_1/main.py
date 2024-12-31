#from arbresEntrant import *
#from forkjoin import *
from parallel import *

# =====================================================
#                      PROGRAMME
# =====================================================

'''

#Test pour arbresEntrant 

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

tree = ArbreEntrant(e, [a,c,f])

ordonnancement = [a,b,c,d ,e]

ordonnancementOptimal = ordonnancementArbre(tree)

#print(segment(tree, ordonnancement))
print([node.label for node in ordonnancementOptimal])
print(coutOrdonnancement(tree,ordonnancement))
'''

'''

#Test pour forkJoin

forkTest = forkJoin(2, 8)

c1_1 = Node(3, "c1_1")
c1_2 = Node(4, "c1_2")
c1_3 = Node(5, "c1_3")
c2_1 = Node(4, "c2_1")
c2_2 = Node(7, "c2_2")
c2_3 = Node(8, "c2_3")
c3_1 = Node(12, "c3_1")
c3_2 = Node(11, "c3_2")
c3_3 = Node(1, "c3_3")

forkTest.start_chain(c1_1, 4, 1)

forkTest.add_node(0, c1_2, 2)
forkTest.add_node(0, c1_3, 3)

forkTest.start_chain(c2_1, 3, 4)
forkTest.add_node(1, c2_2, 1)
forkTest.add_node(1, c2_3, 1)

forkTest.start_chain(c3_1, 4, 5)
forkTest.add_node(2, c3_2, 6)
forkTest.add_node(2, c3_3, 6)
minChain = forkTest.minChain()

print([node.label for node in forkTest.ordonnancementForkJoin()])
'''

# Tests pour Série parallèle

# Création des bases
base1 = SP_Base(1,1,"a","b",1)
base2 = SP_Base(1,1,"c","d",1)
base3 = SP_Base(1,1,"a1","b1",1)
base4 = SP_Base(1,1,"c1","d1",1)

# Composition en série
serie = SP_Serie(base1, base2)
serie.print_SP()
#serie2 = SP_Serie(base3, base4)
#serie3 = SP_Serie(serie, serie2)

#ordonnancement = serie3.ordonnancement()
#print("Ordonnancement optimal :", [node.label for node in ordonnancement])

'''
# Composition en parallèle
parallel = SP_Parallel(base1, base2)

complexe = SP_Serie(serie, parallel)
ordonnancement = ordonnancementSerieParallele(complexe)

print("Ordonnancement optimal :", [node.label for node in ordonnancement])
'''