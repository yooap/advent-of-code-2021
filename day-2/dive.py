def part1():
    input = open("input.txt", "r")

    hPos, depth = 0, 0
    commands = {
        "forward": lambda value, hPos, depth: (hPos+value, depth),
        "down": lambda value, hPos, depth: (hPos, depth+value),
        "up": lambda value, hPos, depth: (hPos, depth-value)
    }

    for line in input:
        command, value = parse_line(line)
        hPos, depth = commands[command](value, hPos, depth)
    input.close()
    return hPos*depth


def parse_line(line):
    command_and_value = line.split()
    assert len(command_and_value) == 2
    command = command_and_value[0]
    value = int(command_and_value[1])

    return (command, value)


def part2():
    input = open("input.txt", "r")

    hPos, depth, aim = 0, 0, 0
    commands = {
        "forward": lambda value, hPos, depth, aim: (hPos+value, depth+(aim*value), aim),
        "down": lambda value, hPos, depth, aim: (hPos, depth, aim+value),
        "up": lambda value, hPos, depth, aim: (hPos, depth, aim-value)
    }

    for line in input:
        command, value = parse_line(line)
        hPos, depth, aim = commands[command](value, hPos, depth, aim)
    input.close()
    return hPos*depth


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
