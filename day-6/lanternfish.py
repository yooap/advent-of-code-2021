def part1():
    days = 80
    first_cycle_days = 8
    subsequent_cycle_days = 6
    fish_list = None
    with open("input.txt", "r") as input:
        fish_list = [int(fish) for fish in input.readline().strip().split(",")]

    for day in range(0, days):
        new_fish_count = 0
        for idx, fish in enumerate(fish_list):
            if fish == 0:
                new_fish_count += 1
                fish_list[idx] = subsequent_cycle_days
            else:
                fish_list[idx] = fish - 1
        fish_list.extend([first_cycle_days]*new_fish_count)

    return len(fish_list)


def part2():
    days = 256
    first_cycle_days = 8
    subsequent_cycle_days = 6
    fish_map = {}  # days:count
    with open("input.txt", "r") as input:
        fish_list = [int(fish) for fish in input.readline().strip().split(",")]
        for fish in fish_list:
            current_count = fish_map.get(fish, 0)
            fish_map[fish] = current_count + 1

    for day in range(0, days):
        updated_fish_map = {}
        for fish_day in sorted(fish_map.keys(), reverse=True):
            count = fish_map[fish_day]
            if fish_day == 0:  # will be called last in iteration
                current_count_on_subsequent_cycle_day = updated_fish_map.get(
                    subsequent_cycle_days, 0)
                updated_fish_map[subsequent_cycle_days] = count + \
                    current_count_on_subsequent_cycle_day
                updated_fish_map[first_cycle_days] = count
            else:
                updated_fish_map[fish_day-1] = count
        fish_map = updated_fish_map

    return sum(fish_map.values())


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
