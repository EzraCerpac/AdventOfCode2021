measurements = [int(n) for n in open("input.txt").read().split("\n")]

n_larger = 0

for i in range(len(measurements)):
    if i < 4:
        continue
    elif sum(measurements[i - 2:i + 1]) > sum(measurements[i - 3:i]):
        n_larger += 1

print(n_larger)
