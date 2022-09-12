binary_lst = [[int(n) for n in n_str] for n_str in open("input.txt").read().split("\n")]

oxygen = []
CO2 = []


def most_common_bit(binary_lst: list, position: int) -> int:
    zeros = 0
    ones = 0
    for binary in binary_lst:
        if binary[position] == 0:
            zeros += 1
        else:
            ones += 1
    if zeros > ones:
        return 0
    else:
        return 1


def filter(binary_lst: list, position: int, keep: int) -> list:
    if len(binary_lst) == 1:
        return binary_lst
    new_list = []
    for binary in binary_lst:
        if binary[position] == keep:
            new_list.append(binary)
    if not new_list:
        return [binary_lst[-1]]
    return new_list


def filter_list(binary_lst: list, most: bool) -> list:
    lst = binary_lst
    i = 0
    while len(lst) > 1:
        most_bit = most_common_bit(lst, i)
        keep = abs(1 - most_bit - most)
        lst = filter(lst, i, keep)
        # print(i, most_bit, keep, lst)
        i += 1
    return lst


def binary_to_decimal(binary: list) -> int:
    n = 0
    for bit, one in enumerate(reversed(binary)):
        if one:
            n += 2 ** bit
    return n


if __name__ == '__main__':
    oxygen_binary = filter_list(binary_lst, True)[0]
    CO2_binary = filter_list(binary_lst, False)[0]
    oxygen = binary_to_decimal(oxygen_binary)
    CO2 = binary_to_decimal(CO2_binary)
    life_support = oxygen * CO2
    print(life_support)
