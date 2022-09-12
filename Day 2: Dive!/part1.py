commands = [x.split(" ") for x in open("input.txt").read().split("\n")]

print(commands)

horizontal = 0
depth = 0

for command in commands:
    match command:
        case ["forward", amount]:
            n = int(amount)
            horizontal += n
        case ["down", amount]:
            n = int(amount)
            depth += n
        case ["up", amount]:
            n = int(amount)
            depth -= n

print(horizontal * depth)
