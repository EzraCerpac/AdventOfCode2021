from numpy import median

lines: list[str] = [str.strip('\n') for str in open("input.txt").readlines()]

bracket_dict = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}

points_dict = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}

scores = []
for line in lines:
    open_brackets: list[str] = []
    for bracket in line:
        if bracket in bracket_dict.keys():
            open_brackets.append(bracket)
        elif bracket in bracket_dict.values():
            if bracket == bracket_dict[open_brackets[-1]]:
                del open_brackets[-1]
            else:
                open_brackets = []
                break
        else:
            raise EnvironmentError("Not a bracket")
    if open_brackets:
        open_brackets.reverse()
        closing_brackets = [bracket_dict[bracket] for bracket in open_brackets]
        score = 0
        for bracket in closing_brackets:
            score *= 5
            score += points_dict[bracket]
        scores.append(score)
print(int(median(scores)))
