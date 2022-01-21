def part1():
    octopi = parse_input()
    flashes = 0
    steps = 100
    for step in range(0, steps):
        for y, row in enumerate(octopi):
            for x, level in enumerate(row):
                increment(octopi, y, x)

        for y, row in enumerate(octopi):
            for x, level in enumerate(row):
                if level > 9:
                    flashes += flash(octopi, y, x)
    return flashes


def part2():
    octopi = parse_input()
    step = 1
    while True:
        flashes_in_step = 0
        for y, row in enumerate(octopi):
            for x, level in enumerate(row):
                increment(octopi, y, x)

        for y, row in enumerate(octopi):
            for x, level in enumerate(row):
                if level > 9:
                    flashes_in_step += flash(octopi, y, x)

        if flashes_in_step == 100:
            return step

        step += 1


def parse_input():
    octopi = []
    with open("input.txt", "r") as input:
        for line in input:
            octopi.append([int(level) for level in list(line.strip())])
    return octopi


def increment(octopi, y, x):
    octopi[y][x] = octopi[y][x] + 1


def flash(octopi, y, x):
    flashes = 1
    octopi[y][x] = 0
    top = y - 1
    right = x + 1
    bottom = y + 1
    left = x - 1
    top_available = top >= 0
    right_available = right <= 9
    bottom_available = bottom <= 9
    left_available = left >= 0

    # top
    if top_available and octopi[top][x] != 0:
        increment(octopi, top, x)
        if (octopi[top][x] > 9):
            flashes += flash(octopi, top, x)

    # top right
    if top_available and right_available and octopi[top][right] != 0:
        increment(octopi, top, right)
        if (octopi[top][right] > 9):
            flashes += flash(octopi, top, right)

    # right
    if right_available and octopi[y][right] != 0:
        increment(octopi, y, right)
        if (octopi[y][right] > 9):
            flashes += flash(octopi, y, right)

    # bottom right
    if bottom_available and right_available and octopi[bottom][right] != 0:
        increment(octopi, bottom, right)
        if (octopi[bottom][right] > 9):
            flashes += flash(octopi, bottom, right)

    # bottom
    if bottom_available and octopi[bottom][x] != 0:
        increment(octopi, bottom, x)
        if (octopi[bottom][x] > 9):
            flashes += flash(octopi, bottom, x)

    # bottom left
    if bottom_available and left_available and octopi[bottom][left] != 0:
        increment(octopi, bottom, left)
        if (octopi[bottom][left] > 9):
            flashes += flash(octopi, bottom, left)

    # left
    if left_available and octopi[y][left] != 0:
        increment(octopi, y, left)
        if (octopi[y][left] > 9):
            flashes += flash(octopi, y, left)

    # top left
    if top_available and left_available and octopi[top][left] != 0:
        increment(octopi, top, left)
        if (octopi[top][left] > 9):
            flashes += flash(octopi, top, left)

    return flashes


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
