def part1():
    heightmap = parse_input()
    low_points = get_low_points(heightmap)
    result = sum([heightmap[low_point[0]][low_point[1]] + 1
                  for low_point in low_points])
    return result


def part2():
    heightmap = parse_input()
    low_points = get_low_points(heightmap)
    basins = []
    for low_point in low_points:
        basin = set()
        calculate_basin(heightmap, low_point, basin)
        basins.append(basin)
    basin_sizes = [len(basin) for basin in basins]
    basin_sizes.sort(reverse=True)
    largest_basin_sizes = basin_sizes[0:3]
    result = 1
    for size in largest_basin_sizes:
        result *= size
    return result


def parse_input():
    heightmap = []
    with open("input.txt", "r") as input:
        for line in input:
            heightmap_row = [int(height) for height in list(line.strip())]
            heightmap.append(heightmap_row)
    return heightmap


def get_low_points(heightmap):
    low_points = []
    for y, row in enumerate(heightmap):
        for x, height in enumerate(row):
            if y != 0:
                top = heightmap[y-1][x]
                if top <= height:
                    continue
            if x != len(row) - 1:
                right = heightmap[y][x+1]
                if right <= height:
                    continue
            if y != len(heightmap) - 1:
                bottom = heightmap[y+1][x]
                if bottom <= height:
                    continue
            if x != 0:
                left = heightmap[y][x-1]
                if left <= height:
                    continue
            low_points.append((y, x))
    return low_points


def calculate_basin(heightmap, location, basin):
    if location in basin:
        return

    y, x = location
    height = heightmap[y][x]
    if height == 9:
        return

    basin.add(location)

    if y != 0:
        top = heightmap[y-1][x]
        if top > height:
            calculate_basin(heightmap, (y-1, x), basin)
    if x != len(heightmap[y]) - 1:
        right = heightmap[y][x+1]
        if right > height:
            calculate_basin(heightmap, (y, x+1), basin)
    if y != len(heightmap) - 1:
        bottom = heightmap[y+1][x]
        if bottom > height:
            calculate_basin(heightmap, (y+1, x), basin)
    if x != 0:
        left = heightmap[y][x-1]
        if left > height:
            calculate_basin(heightmap, (y, x-1), basin)

    return basin


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
