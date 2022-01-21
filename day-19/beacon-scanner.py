def part1():
    scanners = parse_input()
    base_scanner = scanners.pop(0)
    scanners_to_check_against_as_base = [base_scanner]
    checked_base_scanners = []
    all_beacons = set(beacon for beacon in base_scanner)

    while len(scanners):
        base_scanner = scanners_to_check_against_as_base.pop()
        scanners_to_still_check = []
        for scanner in scanners:
            normalized_beacons = find_correct_transformation(
                base_scanner, scanner)[0]
            if normalized_beacons != None:
                all_beacons.update(normalized_beacons)
                if normalized_beacons not in checked_base_scanners:
                    scanners_to_check_against_as_base.append(
                        normalized_beacons)
            else:
                scanners_to_still_check.append(scanner)
        scanners = scanners_to_still_check
        checked_base_scanners.append(base_scanner)

    return len(all_beacons)


def part2():
    scanners = parse_input()
    scanner_distances_from_origin = [(0, 0, 0)]
    base_scanner = scanners.pop(0)
    scanners_to_check_against_as_base = [base_scanner]
    checked_base_scanners = []

    while len(scanners):
        base_scanner = scanners_to_check_against_as_base.pop()
        scanners_to_still_check = []
        for scanner in scanners:
            normalized_beacons, distance = find_correct_transformation(
                base_scanner, scanner)
            if normalized_beacons != None:
                scanner_distances_from_origin.append(distance)
                if normalized_beacons not in checked_base_scanners:
                    scanners_to_check_against_as_base.append(
                        normalized_beacons)
            else:
                scanners_to_still_check.append(scanner)
        scanners = scanners_to_still_check
        checked_base_scanners.append(base_scanner)

    max_manhattan_distance = 0
    for d1 in scanner_distances_from_origin:
        for d2 in scanner_distances_from_origin:
            manhattan_distance = sum([abs(coord1-coord2)
                                     for coord1, coord2 in zip(d1, d2)])
            if manhattan_distance > max_manhattan_distance:
                max_manhattan_distance = manhattan_distance

    return max_manhattan_distance


def parse_input():
    scanners = []
    with open("input.txt", "r") as input:
        for unescaped_line in input:
            line = unescaped_line.strip()
            if line:
                if line.startswith("---"):
                    scanners.append([])
                else:
                    scanner = scanners[-1]
                    scanner.append(tuple([int(coord)
                                   for coord in line.split(",")]))
    return scanners


def find_correct_transformation(base_scanner, scanner):
    for axis_flips in [(1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1), (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1)]:
        for axis_positions in [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]:
            transformed_scanner = transform(
                scanner, axis_flips, axis_positions)
            distance, beacons_in_base_coord = overlaps(
                base_scanner, transformed_scanner)
            if (distance != None):
                beacons_in_base_coord = [
                    tuple(beacon[i]+distance[i] for i in range(3)) for beacon in transformed_scanner]
                return beacons_in_base_coord, distance
    return None, None


def transform(scanner, axis_flips, axis_pos):
    transformed_scanner = []
    for beacon in scanner:
        transformed_beacon = tuple(beacon[i]*axis_flips[i] for i in range(3))
        transformed_beacon = tuple(
            transformed_beacon[axis_pos[i]] for i in range(3))
        transformed_scanner.append(transformed_beacon)
    return transformed_scanner


def overlaps(base_scanner, scanner):
    distances = {}
    for base_scanner_beacon in base_scanner:
        for scanner_beacon in scanner:
            distance = distance_between_beacons(
                base_scanner_beacon, scanner_beacon)
            if distance in distances:
                distances[distance] = distances[distance] + 1
            else:
                distances[distance] = 1

    valid_distances = [(distance, value)
                       for distance, value in distances.items() if value >= 12]
    if len(valid_distances) > 0:
        valid_distances.sort(key=lambda x: x[0])
        distance_between_scanners = valid_distances[-1][0]
        non_overlaping_beacons = []
        for base_scanner_beacon in base_scanner:
            for scanner_beacon in scanner:
                distance = distance_between_beacons(
                    base_scanner_beacon, scanner_beacon)
                if distance != distance_between_scanners:
                    non_overlaping_beacons.append(scanner_beacon)
        return distance_between_scanners, non_overlaping_beacons
    else:
        return None, None


def distance_between_beacons(base_scanner_beacon, scanner_beacon):
    return tuple(b1 - b2 for b1, b2 in zip(base_scanner_beacon, scanner_beacon))


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
