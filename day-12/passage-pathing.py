def part1():
    connections = parse_input()
    paths = [["start"]]
    while has_open_paths(paths):
        updated_paths = []
        for path in paths:
            last_location = path[-1]
            if last_location == "end":
                updated_paths.append(path)
            else:
                destinations = connections[last_location]
                for destination in destinations:
                    if not valid_destination(destination, path):
                        continue
                    updated_path = path.copy()
                    updated_path.append(destination)
                    updated_paths.append(updated_path)
        paths = updated_paths

    return len(paths)


def part2():
    connections = parse_input()
    paths = [["start"]]
    while has_open_paths(paths):
        updated_paths = []
        for path in paths:
            last_location = path[-1]
            if last_location == "end":
                updated_paths.append(path)
            else:
                destinations = connections[last_location]
                for destination in destinations:
                    if not valid_destination_v2(destination, path):
                        continue
                    updated_path = path.copy()
                    updated_path.append(destination)
                    updated_paths.append(updated_path)
        paths = updated_paths

    return len(paths)


def parse_input():
    connections = {}
    with open("input.txt", "r") as input:
        for line in input:
            connection_a, connection_b = line.strip().split("-")
            add_connection(connections, connection_a, connection_b)
            add_connection(connections, connection_b, connection_a)
    return connections


def add_connection(connections, connection_in, connection_out):
    if connection_in == "end" or connection_out == "start":
        return
    destinations = connections.get(connection_in, set())
    destinations.add(connection_out)
    connections[connection_in] = destinations


def has_open_paths(paths):
    for path in paths:
        if path[-1] != "end":
            return True
    return False


def valid_destination(destination, path):
    if destination.islower():
        return not destination in path
    return True


def valid_destination_v2(destination, path):
    if destination.islower():
        return not destination in path or not has_any_small_cave_been_visited_twice(path)
    return True


def has_any_small_cave_been_visited_twice(path):
    visited_small_caves = [location for location in path if location.islower()]
    return len(visited_small_caves) != len(set(visited_small_caves))


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
