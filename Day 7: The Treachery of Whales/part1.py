import numpy as np

positions = np.array([int(x) for x in open("input.txt").readline().split(',')])
# positions = np.array([16,1,2,0,4,2,7,1,2,14])

aligned_pos = np.median(positions)

fuel = abs(positions - aligned_pos)

print(sum(fuel))