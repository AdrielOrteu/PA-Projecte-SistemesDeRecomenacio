import numpy as np

arr = np.array([52,5,36,2,7,238,9,3,654,1,33,6,4,15,95,2])
print(arr)
print(np.array([2,3,4,5,6,7,8,9,10,11,12,13,14,15,0,1]))
print(arr[np.array([2,3,4,5,6,7,8,9,10,11,12,13,14,15,0,1])])
print("######")
print(arr)
print(np.argsort(arr))
print(arr[np.argsort(arr)])


# np.argsort(arr)
# np.array([2,3,4,5,6,7,8,9,10,11,12,13,14,15,0,1])