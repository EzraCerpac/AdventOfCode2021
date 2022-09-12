binary_lst = [[int(n) for n in n_str] for n_str in open("input.txt").read().split("\n")]

gamma = []
epsilon = []

for i in range(len(binary_lst[0])):
    zeros = 0
    ones = 0
    for binary in binary_lst:
        if binary[i] == 0:
            zeros += 1
        else:
            ones += 1
    if zeros > ones:
        gamma.append(0)
        epsilon.append(1)
    elif ones > zeros:
        gamma.append(1)
        epsilon.append(0)
    else:
        raise ValueError(f"equal amount of zero's and ones in {i}-th bit.")


def binary_to_decimal(binary: list) -> int:
    n = 0
    for bit, one in enumerate(reversed(binary)):
        if one:
            n += 2 ** bit
    return n


if __name__ == '__main__':
    gamma_rate = binary_to_decimal(gamma)
    epsilon_rate = binary_to_decimal(epsilon)
    print(gamma_rate * epsilon_rate)
