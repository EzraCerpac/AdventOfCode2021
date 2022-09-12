from fish import Fish

timer_lst = [int(x) for x in open("input.txt").readline().split(',')]
# timer_lst = [3,4,3,1,2]

fish_group: list[Fish] = []
for timer in timer_lst:
    fish_group.append(Fish(timer))

days = 80

for day in range(1, days+1):
    for fish in fish_group:
        fish.progress(fish_group)
    print(day)

print(len(fish_group))

