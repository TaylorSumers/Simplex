import math

print("Введите количество переменных")
m = int(input())
print("Введите количество уравнений")
n = int(input())
'''
A = [0] * (n+1)
for i in range(n+1):
    A[i] = [0] * (m+1)

print("Ввод коэффициентов ограничений")
for i in range(n):
    for j in range(m):
        print("а{}{}=".format(i+1, j+1), end='')
        A[i][j] = float(input())

print("Ввод коэффициентов целевой функции")
for j in range(m):
    print("c{}=".format(j+1), end='')
    A[n][j] = float(input())

print("Ввод свободных членов")
for i in range(n+1):
    print("b{}=".format(i+1), end='')
    A[i][m] = float(input())
'''
A = [[1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 6.0], [0.0, 1.0, 2.0, 0.0, 1.0, 0.0, 5.0], [2.0, -1.0, 0.0, 0.0, 0.0, 1.0, 3.0], [-5.0, -6.0, 3.0, 0.0, 0.0, 0.0, 0.0]]
isOptimal=False
while isOptimal!=True:
    rCol=0
    maxEl = 0
    for j in range (m):
        if A[n][j]<0 and abs(A[n][j])>maxEl:
            maxEl = abs(A[n][j])
            rCol = j

    rRow = 0
    minEl = 1000
    for i in range (n):
        if A[i][rCol]>0 and (A[i][m]/A[i][rCol])<minEl:
            minEl = A[i][m]/A[i][rCol]
            rRow = i

    rEl = A[rRow][rCol]
    print(rEl, rCol, rRow)

    NewA = [None] * (n + 1)
    for i in range(n + 1):
        NewA[i] = [None] * (m + 1)

    for i in range(n+1):
        if i != rRow:
            NewA[i][rCol] = 0

    for j in range(m+1):
        NewA[rRow][j] = A[rRow][j]/rEl

    for i in range(n+1):
        if A[i][rCol] == 0:
            for j in range (m+1):
                NewA[i][j]=A[i][j]

    print("/")
    for i in range(n+1):
        for j in range(m+1):
            print("{} ".format(A[i][j]), end='')
        print()
    print("/")

    for i in range(n+1):
        for j in range(m+1):
            print("{} ".format(NewA[i][j]), end='')
        print()

    for i in range(n+1):
        for j in range(m+1):
            if NewA[i][j] == None:
                if i == (n) and j == (m):
                    NewA[i][j] = A[i][j] + A[i][rCol]*NewA[rRow][j]
                else:
                    NewA[i][j] = A[i][j] - A[i][rCol] * NewA[rRow][j]
    for i in range(n+1):
        for j in range(m+1):
            print("{} ".format(NewA[i][j]), end='')
        print()

    isOptimal = True
    for i in range(n):
        if NewA[i][m]<0:
            isOptimal = False
    for j in range(m):
        if NewA[n][j]<0:
            isOptimal = False

    for i in range(n+1):
        for j in range(m+1):
            A[i][j]=NewA[i][j]
    print("it end")

