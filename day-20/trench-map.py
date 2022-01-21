def part1():
    algorithm, image = parse_input()
    for i in range(2):
        image = enhance_image(algorithm, image)
    return count_lit_pixels(image)


def part2():
    algorithm, image = parse_input()
    for i in range(50):
        image = enhance_image(algorithm, image)
    return count_lit_pixels(image)


def parse_input():
    algorithm, image = None, []
    with open("input.txt", "r") as input:
        algorithm = input.readline().strip()
        input.readline()
        for line in input:
            image.append(list(line.strip()))

    global switch_outer_pixel_value_on_iteration
    if algorithm[0] == LIT_PIXEL:
        switch_outer_pixel_value_on_iteration = True

    return algorithm, image


def enhance_image(algorithm, image):
    surround_image_with_extra_pixels(image)

    enhanced_image = []
    for y, line in enumerate(image):
        enhanced_image.append([])
        for x, pixel in enumerate(line):
            enhanced_image[y].append(enhance_pixel(y, x, image, algorithm))

    if switch_outer_pixel_value_on_iteration:
        global outer_pixel_value
        outer_pixel_value = LIT_PIXEL if outer_pixel_value == EMPTY_PIXEL else EMPTY_PIXEL

    return enhanced_image


def print_image(image):
    print("\n" + "\n".join(["".join(row) for row in image]))


def surround_image_with_extra_pixels(image: list):
    expand_by = 1
    x_max = max_coord(image)[1]

    for row in image:
        for _ in range(expand_by):
            row.insert(0, outer_pixel_value)
            row.append(outer_pixel_value)

    for _ in range(expand_by):
        image.insert(0, [outer_pixel_value] * (x_max + 1 + expand_by*2))
        image.append(image[0].copy())


def enhance_pixel(y, x, image, algorithm):
    pixel_grid_coord = [(y-1, x-1), (y-1, x), (y-1, x+1),
                        (y, x-1), (y, x), (y, x+1),
                        (y+1, x-1), (y+1, x), (y+1, x+1)]
    value = ""
    for pixel_coord in pixel_grid_coord:
        value = value + value_at_pixel(pixel_coord, image)
    value_bin = to_binary(value)
    return algorithm[int(value_bin, 2)]


def value_at_pixel(pixel_coord, image):
    y, x = pixel_coord
    y_max, x_max = max_coord(image)
    if 0 <= y <= y_max:
        if 0 <= x <= x_max:
            return image[y][x]
    return outer_pixel_value


def max_coord(image):
    return len(image) - 1, len(image[0]) - 1


def to_binary(value: str):
    return value.replace(EMPTY_PIXEL, "0").replace(LIT_PIXEL, "1")


def count_lit_pixels(image):
    count = 0
    for row in image:
        for pixel in row:
            if pixel == LIT_PIXEL:
                count += 1
    return count


EMPTY_PIXEL = "."
LIT_PIXEL = "#"
switch_outer_pixel_value_on_iteration = False
outer_pixel_value = EMPTY_PIXEL

if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
