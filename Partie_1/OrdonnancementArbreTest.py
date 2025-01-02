from arbresEntrant import *

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

print("l'ordonnancement de l'arbre est",[node.label for node in ordonnancementArbre(tree)])