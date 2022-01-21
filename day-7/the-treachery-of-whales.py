def part1():
    crabs = None
    with open("input.txt", "r") as input:
        crabs = parse_input(input)
    possible_fuel_usage = []
    range_start = min(crabs)
    range_end = max(crabs)
    for location in range(range_start, range_end+1):
        used_fuel = 0
        for crab in crabs:
            used_fuel += abs(location-crab)
        possible_fuel_usage.append(used_fuel)
    return min(possible_fuel_usage)


def part2():
    crabs = None
    with open("input.txt", "r") as input:
        crabs = parse_input(input)
    possible_fuel_usage = []
    range_start = min(crabs)
    range_end = max(crabs)
    for location in range(range_start, range_end+1):
        used_fuel = 0
        for crab in crabs:
            steps = abs(location-crab)
            used_fuel += int(steps*(steps+1)/2) # arithmetic series
        possible_fuel_usage.append(used_fuel)
    return min(possible_fuel_usage)

def parse_input(input):
    return [int(crab) for crab in input.readline().strip().split(",")]


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
