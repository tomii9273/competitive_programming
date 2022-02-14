# Lに含まれない最小の非負整数を返す
def mex(L):
    A = [0] * (len(L) + 1)
    for i in L:
        if i < len(A):
            A[i] = 1
    for i in range(len(A)):
        if A[i] == 0:
            return i
