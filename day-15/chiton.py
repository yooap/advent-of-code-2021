def part1():
    cave = parse_input()
    y_max, x_max = len(cave)-1, len(cave[0])-1
    dijkstra_result = dijkstra(cave, y_max, x_max)
    return dijkstra_result[y_max][x_max]


def part2():
    cave = parse_input()
    expand_to = 5
    for row in cave:
        orignal_row = row.copy()
        for i in range(1, expand_to):
            row_expansion = [(level + i if level + i <= 9 else (level + i) % 9)
                             for level in orignal_row]
            row.extend(row_expansion)

    orignal_cave = copy_2d_list(cave)
    for i in range(1, expand_to):
        column_expansion = copy_2d_list(orignal_cave)
        for y, row in enumerate(column_expansion):
            for x, level in enumerate(row):
                column_expansion[y][x] = level + \
                    i if level + i <= 9 else (level + i) % 9
        cave.extend(column_expansion)

    y_max, x_max = len(cave)-1, len(cave[0])-1
    dijkstra_result = dijkstra(cave, y_max, x_max)
    return dijkstra_result[y_max][x_max]


def copy_2d_list(list):
    return [x[:] for x in list]


def dijkstra(cave, y_max, x_max):
    start, end = (0, 0), (y_max, x_max)
    dijkstra = [([None] * (x_max+1)) for y in range(y_max+1)]
    dijkstra[0][0] = 0
    visited = set()

    visit_queue = [start]
    while len(visit_queue) != 0:
        visit(visit_queue, end, visited, cave, dijkstra)

    return dijkstra


def visit(visit_queue, end, visited, cave, dijkstra):
    point = visit_queue.pop(-1)
    if point == end:
        visited.add(end)
        return

    if point in visited:
        return

    y, x = point
    visitable_points = {(y-1, x), (y, x+1), (y+1, x), (y, x-1)}
    visitable_points = filter_invalid_points(visitable_points, end)

    for visitable_point in visitable_points:
        visitable_point_y = visitable_point[0]
        visitable_point_x = visitable_point[1]
        visitable_point_value = cave[visitable_point_y][visitable_point_x]
        current_point_score = dijkstra[y][x]
        score_this_visit = current_point_score + visitable_point_value
        current_visitable_point_score = dijkstra[visitable_point_y][visitable_point_x]
        if current_visitable_point_score == None or score_this_visit < current_visitable_point_score:
            dijkstra[visitable_point_y][visitable_point_x] = score_this_visit
            visited.discard(visitable_point)

    visitable_points.difference_update(visited)

    visited.add(point)
    
    visit_queue_extension = list(visitable_points)
    visit_queue_extension.sort(key=lambda point: dijkstra[point[0]][point[1]], reverse=True)
    visit_queue.extend(visit_queue_extension)



def filter_invalid_points(points, max):
    y_max, x_max = max
    valid = set()
    for point in points:
        if 0 <= point[0] <= y_max and 0 <= point[1] <= x_max:
            valid.add(point)
    return valid


def parse_input():
    cave = []
    with open("message.txt", "r") as input:
        for line in input:
            cave.append([int(level) for level in line.strip()])
    return cave


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
