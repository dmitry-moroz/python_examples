import itertools

def matrixRegionSum2(matr, a, d):
    new_matr = map(lambda r: r[a[1]:d[1]+1], matr[a[0]:d[0]+1])
    #return sum(reduce(lambda x, y: x + y, new_matr))
    return sum(itertools.chain(*new_matr))

if __name__ == '__main__':
    matr = [
        [12, 56, 88, 37, 43, 44, 25, 13],
        [45, 82, 49, 12, 67, 82, 10, 40],
        [37, 93, 25, 70, 15, 38, 39, 29],
        [47, 96, 56, 27, 58, 68, 72, 90],
    ]
    print matrixRegionSum2(matr, (1, 1), (2, 6))
