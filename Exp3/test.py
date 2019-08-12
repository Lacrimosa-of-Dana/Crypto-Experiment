def rev(a, n):
    rmax = []
    cmax = []
    max_t = 0
    for k in range(n):
        max_t = 0
        for i in range(k, n):
            for j in range(k, n):
                if a[i][j] > max_t:
                    max_t = a[i][j]
                    rmax.append(i)
                    cmax.append(j)
                    
        if max_t == 0:
            print("Matrix illegal.")
            return

        if rmax[k] != k:
            for j in range(n):
                a[k][j], a[rmax[k]][j] = a[rmax[k]][j], a[k][j]
        if cmax[k] != k:
            for i in range(n):
                a[i][k], a[i][cmax[k]] = a[i][cmax[k]], a[i][k]

        for j in range(n):
            if j != k:
                a[k][j] = a[k][j] * a[k][k]
        for i in range(n):
            if i != k:
                for j in range(n):
                    if j != k:
                        a[i][j] = a[i][j] ^ (a[i][k]*a[k][j])
        for i in range(n):
            if i != k:
                a[i][k]=a[i][k]*a[k][k]

    for k in range(n - 1, -1, -1):
        if cmax[k] != k:
            for j in range(n):
                a[k][j], a[cmax[k]][j] = a[cmax[k]][j], a[k][j]
            if rmax[k] != k:
                for i in range(n):
                    a[i][k], a[i][rmax[k]] = a[i][rmax[k]], a[i][k]

a = [[1, 1, 0, 0],[1, 0, 1, 0],[0, 0, 1, 1],[0, 1, 0, 0]]
rev(a, 4)
print(a)

    
