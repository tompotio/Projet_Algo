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

solution = ['s', 'c1_1', 'c2_1', 'c2_2', 'c3_1', 'c3_2', 'c2_3', 'c1_2', 'c1_3', 'c3_3', 't']

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

print()
para2.print_SP()

#print([str(weight) for weight in chaine3.registry.list_weights().values()])

ordonnancement = para2.ordonnancement()

print("\nOrdonnancement optimal :", [node.label for node in ordonnancement])
print("Ordonnancement attendu :", solution)

echec = False
for i in range(len(ordonnancement)):
    if not (ordonnancement[i].label == solution[i]):
        echec = True
        break

if echec:
    print("\nEchec")
else:
    print("\nSucces")