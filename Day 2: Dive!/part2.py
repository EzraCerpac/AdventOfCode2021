commands = [x.split(" ") for x in open("input.txt").read().split("\n")]

print(commands)

horizontal = 0
depth = 0
aim = 0

for command in commands:
    match command:
        case ["forward", amount]:
            n = int(amount)
            horizontal += n
            depth += aim * n
        case ["down", amount]:
            n = int(amount)
            aim += n
        case ["up", amount]:
            n = int(amount)
            aim -= n

print(horizontal * depth)
