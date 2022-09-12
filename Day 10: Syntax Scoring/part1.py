lines: list[str] = [str.strip('\n') for str in open("input.txt").readlines()]

bracket_dict = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}

points_dict = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

sum = 0
for line in lines:
    open_brackets: list[str] = []
    for bracket in line:
        if bracket in bracket_dict.keys():
            open_brackets.append(bracket)
        elif bracket in bracket_dict.values():
            if bracket == bracket_dict[open_brackets[-1]]:
                del open_brackets[-1]
            else:
                points = points_dict[bracket]
                sum += points
                break
        else:
            raise EnvironmentError("Not a bracket")
print(sum)
