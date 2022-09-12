measurements = [int(n) for n in open("input.txt").read().split("\n")]

n_larger = 0

for i, measurement in enumerate(measurements):
    if i == 0:
        continue
    elif measurement > measurements[i - 1]:
        n_larger += 1

print(n_larger)
