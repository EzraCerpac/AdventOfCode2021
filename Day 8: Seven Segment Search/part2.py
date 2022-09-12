from encryption import Encryption

with open("input.txt") as f:
    lines = f.readlines()
    output_lst = []
    learn_lst = []
    for line in lines:
        input, output = line.split(' | ')
        output = output.strip("\n").split(" ")
        input = input.split(" ")
        output_lst.append(output)
        learn_lst.append(input + output)

encryption_lst = []


def decrypt(signal, crypt: Encryption) -> Encryption:
    print(crypt.segments)
    for number in signal:
        if len(number) in [2, 3, 4, 7]:
            crypt.filter_options(number)
    print(crypt.segments)
    crypt.solve()
    crypt.try_options(signal)
    return crypt


sum = 0
for i, entry in enumerate(learn_lst):
    encryption = Encryption(entry)
    sum += encryption.calc_value(output_lst[i])
print(sum)
