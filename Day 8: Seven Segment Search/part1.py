with open("input.txt") as f:
    lines = f.readlines()
    output_lst = []
    for line in lines:
        input, output = line.split(' | ')
        output = output.strip("\n").split(" ")
        output_lst.append(output)



sum = 0
for output in output_lst:
    for signal in output:
        if len(signal) in [2, 3, 4, 7]:
            sum += 1
print(sum)