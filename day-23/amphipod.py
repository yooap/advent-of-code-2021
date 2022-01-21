def part1():
    field = parse_input()
    finished_totals = []
    states = {}
    do_next_move(field, 0, finished_totals, states)
    return min(finished_totals)


def part2():
    field = parse_input()
    insert_extra_lines(field)
    field = dict(sorted(field.items()))
    finished_totals = []
    states = {}
    do_next_move(field, 0, finished_totals, states, 4)
    return min(finished_totals)


def insert_extra_lines(field):
    # move row 2 two rows down
    for x in [2, 4, 6, 8]:
        field[(4, x)] = field[(2, x)]

    field[(2, 2)] = "D"
    field[(2, 4)] = "C"
    field[(2, 6)] = "B"
    field[(2, 8)] = "A"

    field[(3, 2)] = "D"
    field[(3, 4)] = "B"
    field[(3, 6)] = "A"
    field[(3, 8)] = "C"


def do_next_move(field, total, finished_totals, states, depth=2):
    # do not continue, we have a more optimal path already
    if len(finished_totals) and total >= min(finished_totals):
        return

    if deadlock(field):  # skip some deadlock situations
        return

    key = frozenset(field.items())
    if key in states and states[key] <= total:
        return
    else:
        states[key] = total

    possible_movable_coord = []
    # hallway
    for x in range(11):
        if field[(0, x)] != None:
            possible_movable_coord.append((0, x))
    # rooms
    for x in [2, 4, 6, 8]:
        pods_can_move_out_of_room = room_contains_forein_pods(
            field, depth, x)
        if pods_can_move_out_of_room:
            # pick top pod if any present
            for y in range(1, depth+1):
                if field[(y, x)] != None:
                    possible_movable_coord.append((y, x))
                    break

    for move in possible_movable_coord:
        pod = field[move]
        # can go to their pod
        dest_x = get_column_for_pod_type(pod)
        pod_can_go_to_room = not room_contains_forein_pods(
            field, depth, dest_x)
        if pod_can_go_to_room:
            current_x = move[1]
            blocked = False
            direction = 1 if dest_x > current_x else -1
            for x in range(current_x + direction, dest_x, direction):
                if field[(0, x)] != None:
                    blocked = True
            if blocked == False:
                new_total = total
                # x distance
                multiplier = get_multiplier(pod)
                new_total += abs(dest_x-current_x) * multiplier
                # y out distance
                new_total += move[0] * multiplier
                # y in distance
                for dest_y in range(depth, 0, -1):
                    if field[(dest_y, dest_x)] == None:
                        break
                new_total += dest_y * multiplier
                field_after_move = field.copy()
                field_after_move[move] = None
                field_after_move[(dest_y, dest_x)] = pod
                do_next_move(field_after_move, new_total,
                             finished_totals, states, depth)
                continue

        # go over all pods in rooms
        if move[0] != 0:
            current_x = move[1]
            # go left
            for dest_x in range(current_x-1, -1, -1):
                if is_in_front_of_room(dest_x):
                    continue
                if field[(0, dest_x)] != None:
                    break  # blocked
                new_total = total
                new_total += (abs(dest_x-current_x) +
                              move[0]) * get_multiplier(pod)
                field_after_move = field.copy()
                field_after_move[move] = None
                field_after_move[(0, dest_x)] = pod
                do_next_move(field_after_move, new_total,
                             finished_totals, states, depth)
            # go right
            for dest_x in range(current_x+1, 11):
                if is_in_front_of_room(dest_x):
                    continue
                if field[(0, dest_x)] != None:
                    break  # blocked
                new_total = total
                new_total += (dest_x-current_x + move[0]) * get_multiplier(pod)
                field_after_move = field.copy()
                field_after_move[move] = None
                field_after_move[(0, dest_x)] = pod
                do_next_move(field_after_move, new_total,
                             finished_totals, states, depth)

    if winning_state(field, depth):
        finished_totals.append(total)


def room_contains_forein_pods(field, depth, room):
    pod_types_in_room = set()
    for y in range(1, depth+1):
        pod = field[(y, room)]
        pod_types_in_room.add(pod)
    pod_types_in_room.discard(None)
    pod_types_in_room.discard(get_pod_type_for_column(room))
    return len(pod_types_in_room) > 0


def deadlock(field):
    # 0,3 in deadlock
    if field[(0, 3)] == "D":
        if field[(0, 5)] == "A" or field[(0, 7)] == "A":
            return True

    if field[(0, 3)] == "C":
        if field[(0, 5)] == "A":
            return True

    # 0,5 in deadlock
    if field[(0, 5)] == "D":
        if field[(0, 7)] in ("A", "B"):
            return True

    if field[(0, 5)] == "A":
        if field[(0, 3)] in ("C", "B"):
            return True

    # 0,7 in deadlock
    if field[(0, 7)] == "A":
        if field[(0, 5)] == "D" or field[(0, 7)] == "D":
            return True

    if field[(0, 7)] == "B":
        if field[(0, 5)] == "D":
            return True

    return False


def is_in_front_of_room(row):
    return row in [2, 4, 6, 8]


def get_pod_type_for_column(column):
    return {
        2: "A",
        4: "B",
        6: "C",
        8: "D",
    }[column]


def get_column_for_pod_type(pod):
    return {
        "A": 2,
        "B": 4,
        "C": 6,
        "D": 8,
    }[pod]


def get_multiplier(pod):
    return {
        "A": 1,
        "B": 10,
        "C": 100,
        "D": 1000,
    }[pod]


def winning_state(field, depth):
    for y in range(1, depth+1):
        for x in [2, 4, 6, 8]:
            if field[(y, x)] != get_pod_type_for_column(x):
                return False

    return True


def parse_input():
    field = {
        (0, 0): None,
        (0, 1): None,
        (0, 2): None,
        (0, 3): None,
        (0, 4): None,
        (0, 5): None,
        (0, 6): None,
        (0, 7): None,
        (0, 8): None,
        (0, 9): None,
        (0, 10): None,
        (1, 2): None,
        (2, 2): None,
        (1, 4): None,
        (2, 4): None,
        (1, 6): None,
        (2, 6): None,
        (1, 8): None,
        (2, 8): None
    }
    with open("input.txt", "r") as input:
        lines = input.readlines()[2:4]
        lines_clean = [line.replace(" ", "").replace("#", "")
                       for line in lines]
        field[(1, 2)] = lines_clean[0][0]
        field[(1, 4)] = lines_clean[0][1]
        field[(1, 6)] = lines_clean[0][2]
        field[(1, 8)] = lines_clean[0][3]
        field[(2, 2)] = lines_clean[1][0]
        field[(2, 4)] = lines_clean[1][1]
        field[(2, 6)] = lines_clean[1][2]
        field[(2, 8)] = lines_clean[1][3]
    return field


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
