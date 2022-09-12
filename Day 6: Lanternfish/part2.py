timer_lst = [int(x) for x in open("input.txt").readline().split(',')]

days = 256

n_new_fish: dict[int:int] = {}

for timer in range(9):
    n = timer_lst.count(timer)
    n_new_fish[timer] = n

for day in range(1, days+1):
    n_new_fish[9] = n_new_fish[0]
    n_new_fish[7] += n_new_fish[0]
    for timer in n_new_fish.keys():
        if timer:
            n_new_fish[timer-1] = n_new_fish[timer]
    del n_new_fish[9]

print(sum(n_new_fish.values()))
