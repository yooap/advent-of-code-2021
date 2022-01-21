def part1():
    dots, instructions = parse_input()
    instruction = instructions[0]
    dots = fold(dots, instruction)
    return len(dots)


def part2():
    dots, instructions = parse_input()
    for instruction in instructions:
        dots = fold(dots, instruction)

    paper = dots_to_paper(dots)
    return paper


def parse_input():
    dots, instructions = set(), list()
    with open("input.txt", "r") as input:
        for unstripped_line in input:
            line = unstripped_line.strip()
            if line:
                if line.startswith("fold along"):
                    axis, value = line[11:].split("=")
                    instructions.append((axis, int(value)))
                else:
                    x, y = line.split(",")
                    dots.add((int(x), int(y)))

    return dots, instructions


def fold(dots, instruction):
    updated_dots = set()
    axis, value = instruction
    if axis == "y":
        for dot in dots:
            x, y = dot
            if y < value:
                updated_dots.add(dot)
            else:
                new_y = value - (y - value)
                updated_dots.add((x, new_y))
    else:
        for dot in dots:
            x, y = dot
            if x < value:
                updated_dots.add(dot)
            else:
                new_x = value - (x - value)
                updated_dots.add((new_x, y))
    return updated_dots


def dots_to_paper(dots):
    x_max = max(dot[0] for dot in dots)
    y_max = max(dot[1] for dot in dots)
    paper_map = [["."] * (x_max+1) for y in range(y_max+1)]
    for dot in dots:
        paper_map[dot[1]][dot[0]] = "#"

    paper_string = "\n"
    for row in paper_map:
        for value in row:
            paper_string += value
        paper_string += "\n"
    return paper_string


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
