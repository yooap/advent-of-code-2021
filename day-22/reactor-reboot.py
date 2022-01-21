def part1():
    steps = parse_input()
    on_cubes = set()
    min_max = (-50, 50)
    for step in steps:
        operation, coords = step
        x_coords, y_coords, z_coords = coords
        cubes = set()
        for x_coord in coord_range(x_coords, min_max):
            for y_coord in coord_range(y_coords, min_max):
                for z_coord in coord_range(z_coords, min_max):
                    cubes.add((x_coord, y_coord, z_coord))

        if operation:
            on_cubes.update(cubes)
        else:
            on_cubes.difference_update(cubes)
    return len(on_cubes)


def part2():
    steps = parse_input()
    on_areas = []
    for step in steps:
        operation, area = step
        new_on_areas = []
        for on_area in on_areas:
            split_result = split_area_if_overlaps(on_area, area)
            new_on_areas.extend(split_result)
        if operation:
            new_on_areas.append(area)
        on_areas = new_on_areas

    total = 0
    for on_area in on_areas:
        x_range, y_range, z_range = on_area
        total += (abs(x_range[0] - x_range[1]) + 1) * \
            (abs(y_range[0] - y_range[1]) + 1) * \
            (abs(z_range[0] - z_range[1]) + 1)

    return total


def parse_input():
    steps = []
    with open("input.txt", "r") as input:
        for line in input:
            operation, coords = line.strip().split()
            x_coords, y_coords, z_coords = [tuple(int(i) for i in coord.split(
                "=")[1].split("..")) for coord in coords.split(",")]
            operation = 1 if operation == "on" else 0
            step = (operation, (x_coords, y_coords, z_coords))
            steps.append(step)
    return steps


def coord_range(coords, min_max=None):
    start, end = coords
    if min_max != None:
        min_threshold, max_threshold = min_max
        if start > max_threshold or end < min_threshold:
            return range(0)
        start, end = max(start, min_threshold), min(end, max_threshold)
    return range(start, end+1)


def split_area_if_overlaps(area_to_split, splitter):
    if is_consumed_by(area_to_split, splitter):
        return []

    if does_not_overlap(area_to_split, splitter):
        return [area_to_split]

    subject_x_coords, subject_y_coords, subject_z_coords = area_to_split
    splitter_x_coords, splitter_y_coords, splitter_z_coords = splitter

    cuts = []

    # cut off by z, bottom
    cut_z_coords = None
    if subject_z_coords[0] < splitter_z_coords[0]:
        cut_z_coords = (subject_z_coords[0], splitter_z_coords[0]-1)
        cuts.append((subject_x_coords, subject_y_coords, cut_z_coords))
        remain_z_coords = (splitter_z_coords[0], area_to_split[2][1])
        area_to_split = (area_to_split[0], area_to_split[1], remain_z_coords)
        subject_x_coords, subject_y_coords, subject_z_coords = area_to_split  # update

    # cut off by z, top
    cut_z_coords = None
    if subject_z_coords[1] > splitter_z_coords[1]:
        cut_z_coords = (splitter_z_coords[1]+1, subject_z_coords[1])
        cuts.append((subject_x_coords, subject_y_coords, cut_z_coords))
        remain_z_coords = (area_to_split[2][0], splitter_z_coords[1])
        area_to_split = (area_to_split[0], area_to_split[1], remain_z_coords)
        subject_x_coords, subject_y_coords, subject_z_coords = area_to_split  # update

    # cut off by y, bottom
    cut_y_coords = None
    if subject_y_coords[0] < splitter_y_coords[0]:
        cut_y_coords = (subject_y_coords[0], splitter_y_coords[0]-1)
        cuts.append((subject_x_coords, cut_y_coords, subject_z_coords))
        remain_y_coords = (splitter_y_coords[0], area_to_split[1][1])
        area_to_split = (area_to_split[0], remain_y_coords, area_to_split[2])
        subject_x_coords, subject_y_coords, subject_z_coords = area_to_split  # update

    # cut off by y, top
    cut_y_coords = None
    if subject_y_coords[1] > splitter_y_coords[1]:
        cut_y_coords = (splitter_y_coords[1]+1, subject_y_coords[1])
        cuts.append((subject_x_coords, cut_y_coords, subject_z_coords))
        remain_y_coords = (area_to_split[1][0], splitter_y_coords[1])
        area_to_split = (area_to_split[0], remain_y_coords, area_to_split[2])
        subject_x_coords, subject_y_coords, subject_z_coords = area_to_split  # update

    # cut off by x, bottom
    cut_x_coords = None
    if subject_x_coords[0] < splitter_x_coords[0]:
        cut_x_coords = (subject_x_coords[0], splitter_x_coords[0]-1)
        cuts.append((cut_x_coords, subject_y_coords, subject_z_coords))
        remain_x_coords = (splitter_x_coords[0], area_to_split[0][1])
        area_to_split = (remain_x_coords, area_to_split[1], area_to_split[2])
        subject_x_coords, subject_y_coords, subject_z_coords = area_to_split  # update

    # cut off by x, top
    cut_x_coords = None
    if subject_x_coords[1] > splitter_x_coords[1]:
        cut_x_coords = (splitter_x_coords[1]+1, subject_x_coords[1])
        cuts.append((cut_x_coords, subject_y_coords, subject_z_coords))
        remain_x_coords = (area_to_split[0][0], splitter_x_coords[1])
        area_to_split = (remain_x_coords, area_to_split[1], area_to_split[2])
        subject_x_coords, subject_y_coords, subject_z_coords = area_to_split  # update

    return cuts


def is_consumed_by(area_to_split, splitter):
    subject_x_coords, subject_y_coords, subject_z_coords = area_to_split
    splitter_x_coords, splitter_y_coords, splitter_z_coords = splitter

    return subject_x_coords[0] >= splitter_x_coords[0] and \
        subject_x_coords[1] <= splitter_x_coords[1] and \
        subject_y_coords[0] >= splitter_y_coords[0] and \
        subject_y_coords[1] <= splitter_y_coords[1] and \
        subject_z_coords[0] >= splitter_z_coords[0] and \
        subject_z_coords[1] <= splitter_z_coords[1]


def does_not_overlap(area_to_split, splitter):
    subject_x_coords, subject_y_coords, subject_z_coords = area_to_split
    splitter_x_coords, splitter_y_coords, splitter_z_coords = splitter

    return subject_x_coords[0] > splitter_x_coords[1] or \
        subject_x_coords[1] < splitter_x_coords[0] or \
        subject_y_coords[0] > splitter_y_coords[1] or \
        subject_y_coords[1] < splitter_y_coords[0] or \
        subject_z_coords[0] > splitter_z_coords[1] or \
        subject_z_coords[1] < splitter_z_coords[0]


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
