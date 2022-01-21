def part1():
    input = open("input.txt", "r")
    counter = 0
    last_line = None
    for line in input:
        line_as_int = int(line)
        if last_line != None:
            if line_as_int > last_line:
                counter += 1
        last_line = line_as_int
    input.close()
    return counter


def part2():
    input = open("input.txt", "r")
    groups = 3
    counter = 0
    inputs = []

    for line in input:
        line_as_int = int(line)
        inputs.append(line_as_int)
        if len(inputs) == groups+1:
            last_group_sum = sum(inputs[0:groups])
            current_group_sum = sum(inputs[1:groups+1])
            if current_group_sum > last_group_sum:
                counter += 1
            inputs.pop(0)

    input.close()
    return counter


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
