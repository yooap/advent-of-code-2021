def part1():
    floor_map = parse_input()
    step = 0
    moved = None
    while True:
        step += 1
        moved = move(floor_map)
        if not moved:
            break
    return step


def move(floor_map):
    moved = False
    moved |= move_east(floor_map)
    moved |= move_south(floor_map)
    return moved


def move_east(floor_map):
    skip = set()
    max_x = len(floor_map[0])-1
    for y, row in enumerate(floor_map):
        for x, cucumber in enumerate(row):
            if cucumber != ">" or (y, x) in skip:
                continue
            destination_x = None
            if x < max_x:
                destination_x = x + 1
            else:
                destination_x = 0

            if floor_map[y][destination_x] == "." and (y, destination_x) not in skip:
                floor_map[y][x] = "."
                floor_map[y][destination_x] = ">"
                skip.add((y, destination_x))
                skip.add((y, x))
    return len(skip) > 0


def move_south(floor_map):
    skip = set()
    max_y = len(floor_map)-1
    for y, row in enumerate(floor_map):
        for x, cucumber in enumerate(row):
            if cucumber != "v" or (y, x) in skip:
                continue
            destination_y = None
            if y < max_y:
                destination_y = y + 1
            else:
                destination_y = 0

            if floor_map[destination_y][x] == "." and (destination_y, x) not in skip:
                floor_map[y][x] = "."
                floor_map[destination_y][x] = "v"
                skip.add((y, x))
                skip.add((destination_y, x))
    return len(skip) > 0


def parse_input():
    floor_map = []
    with open("input.txt", "r") as input:
        for line in input:
            floor_map.append(list(line.strip()))
    return floor_map


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
