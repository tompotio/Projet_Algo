def h(i, j, l, hauteurs, largeurs):
    largeurBoite = sum(largeurs[i:j + 1])
    return float('inf') if largeurBoite > l else max(hauteurs[i:j + 1])

def Tmin(obj,l, hauteurs, largeurs):
    nbObjet = len(hauteurs)
    Tmin = [float('inf')] * (nbObjet + 1)
    Tmin[nbObjet] = 0  # Cas de base : aucun objet après le dernier

    # Calcul de Tmin(i) par programmation dynamique
    for i in range(nbObjet - 1, -1, -1):  # De N-1 à 0
        for j in range(i, nbObjet):  # De i à N-1
            Tmin[i] = min(Tmin[i], h(i, j, l, hauteurs, largeurs) + Tmin[j + 1])

    return Tmin[obj-1]

largeur = [1,2,1,1,2,1,3,2]
hauteurs = [1,2,5,4,3,1,2,4]
l = 4
print(f"la hauteur total des carton est {Tmin(1,4,hauteurs,largeur)}")