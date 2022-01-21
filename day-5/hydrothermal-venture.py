def part1():
    grid = []
    with open("input.txt", "r") as input:
        for line in input:
            x1, y1, x2, y2 = get_coordinates(line)
            if x1 == x2:
                y = y1
                while y != y2:
                    update_grid(grid, x1, y)
                    y += 1 if y < y2 else -1
                update_grid(grid, x1, y2)
            elif y1 == y2:
                x = x1
                while x != x2:
                    update_grid(grid, x, y1)
                    x += 1 if x < x2 else -1
                update_grid(grid, x2, y1)

    return count_grid_values(grid, 2)


def part2():
    grid = []
    with open("input.txt", "r") as input:
        for line in input:
            x1, y1, x2, y2 = get_coordinates(line)
            update_grid(grid, x1, y1)
            x, y = x1, y1

            while x != x2 or y != y2:
                x = move_towards(x, x2)
                y = move_towards(y, y2)
                update_grid(grid, x, y)

    return count_grid_values(grid, 2)


def get_coordinates(line):
    coordinates_str = line.strip().replace(" -> ", ",").split(",")
    return [int(i) for i in coordinates_str]


def update_grid(grid, x, y):
    if (len(grid) <= y):
        for i in range(len(grid), y+1):
            grid.append([])

    row = grid[y]
    if (len(row) <= x):
        for i in range(len(row), x+1):
            row.append(0)

    row[x] = row[x] + 1


def count_grid_values(grid, threshold):
    points = 0
    for row in grid:
        for value in row:
            if value >= threshold:
                points += 1
    return points


def move_towards(curr, dest):
    if curr < dest:
        return curr + 1
    if curr > dest:
        return curr - 1
    return curr


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
