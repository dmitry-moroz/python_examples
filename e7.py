def getIndex(currentIndex, N):
    return (currentIndex%3)*N + (currentIndex/3)

def convertArray_extraSpace(arr):
    N=len(arr)/3
    return [arr[getIndex(i, N)] for i in range(len(arr))]


def convertArray(arr):
    res = []
    N=len(arr)/3
    for j in xrange(N):
        for i in xrange(3):
            res.append(arr[j+N*i])
    return res



if __name__ == '__main__':
    arr = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']
    print convertArray_extraSpace(arr)
    print convertArray(arr)
