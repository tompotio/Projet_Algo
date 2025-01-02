def lmin(n,k,widths):
    def l(i,j):
        return sum(widths[i:j+1])
    L = [[float('inf')]*(k+1)  for _ in range(n+1)]

    for v in range(0,k+1):
        L[0][v] = 0
    
    for u in range(1,n+1):
        L[u][1] = l(1,u)
    
    for v in range(1,k + 1):
        for u in range(1,v + 1):
            L[u][v] = max(widths[:u])
    
    for u in range(1,n + 1):
        for v in range(2,min(u,k) + 1):
            for j in range(1,u+1):
                L[u][v] = min(L[u][v],max(L[j-1][v-1],l(j-1,u)))
    return L[n][k]

widths = [1,2,1,1,2,1,3,2]

print(f" la largeur minimal de la configuration {widths} est {lmin(len(widths),3,widths)}")