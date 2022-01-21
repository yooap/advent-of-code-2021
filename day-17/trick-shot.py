def part1():
    target_area = parse_input()
    highest_inital_y_velocity = abs(target_area.y_min) - 1
    return get_peak(highest_inital_y_velocity)


def part2():
    target_area = parse_input()
    return len(possible_velocities(target_area))


def get_peak(inital_y_velocity):
    peak = 0
    y_velocity = inital_y_velocity
    while y_velocity != 0:
        peak += y_velocity
        y_velocity -= 1
    return peak


def possible_velocities(target_area):
    possible_x = possible_x_velocities(target_area)
    possible_y = possible_y_velocities(target_area)
    return combine_possible_xy_velocities(target_area, possible_x, possible_y)


def possible_x_velocities(target_area):
    possible_x = set()
    for x in range(target_area.x_max + 1):
        x_velocity = x
        x_location = x
        # while x veolicty hasnt stopped and we havent over shot
        while x_velocity != 0 and x_location <= target_area.x_max:
            if within_x_bounds(target_area, x_location):
                possible_x.add(x)
                break
            x_velocity -= 1
            x_location += x_velocity
    return possible_x


def within_x_bounds(target_area, x_location):
    return target_area.x_min <= x_location <= target_area.x_max


def possible_y_velocities(target_area):
    possible_y = set()
    y = target_area.y_min
    y_location = y
    # after y arches downward and reaches 0, next step will be negative inital velocity - 1, stop if over shoots
    while y <= 0 or (-y - 1) >= target_area.y_min:
        y_location = y
        y_velocity = y
        while y_location >= target_area.y_min:
            if within_y_bounds(target_area, y_location):
                possible_y.add(y)
                break
            y_velocity -= 1
            y_location += y_velocity
        y += 1
    return possible_y


def within_y_bounds(target_area, y_location):
    return target_area.y_min <= y_location <= target_area.y_max


def combine_possible_xy_velocities(target_area, possible_x, possible_y):
    possible_xy = set()
    for possible_x_vel in possible_x:
        for possible_y_vel in possible_y:
            if reaches_target(target_area, possible_x_vel, possible_y_vel):
                possible_xy.add((possible_x_vel, possible_y_vel))
    return possible_xy


def reaches_target(target_area, initial_x_velocity, initial_y_velocity):
    x_location, y_location = initial_x_velocity, initial_y_velocity
    x_velocity, y_velocity = initial_x_velocity, initial_y_velocity
    while x_location <= target_area.x_max and y_location >= target_area.y_min:
        if within_x_bounds(target_area, x_location) and within_y_bounds(target_area, y_location):
            return True
        x_velocity, y_velocity = 0 if x_velocity == 0 else x_velocity - 1, y_velocity - 1
        x_location, y_location = x_location + x_velocity, y_location + y_velocity
    return False


def parse_input():
    target = None
    with open("input.txt", "r") as input:
        x_and_y_bounds = input.readline().lstrip("target area: ").split(",")
        x_bounds, y_bounds = [to_int_list(bounds.strip().split("=")[1].split(".."))
                              for bounds in x_and_y_bounds]
        target = TargetArea(min(x_bounds), max(x_bounds),
                            min(y_bounds), max(y_bounds))
    return target


def to_int_list(bounds):
    return [int(bound) for bound in bounds]


class TargetArea:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
