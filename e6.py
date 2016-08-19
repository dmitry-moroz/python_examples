def largestContinuousSum(arr):
    if len(arr)==0:
        return
    maxSum=currentSum=arr[0]
    for num in arr[1:]:
        currentSum=max(currentSum + num, num)
        maxSum=max(currentSum, maxSum)
    return maxSum


if __name__ == '__main__':
    arr = [1, 5, -6, 6, 2, -3, -8, 9, 1, -1, 2, -9, 4]
    print largestContinuousSum(arr)
