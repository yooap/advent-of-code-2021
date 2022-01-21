def part1():
    navigation_subsystem = parse_input()

    corrupted_chars = []
    for line in navigation_subsystem:
        open_chars = []
        for char in line:
            if char in opening_chars:
                open_chars.append(char)
            else:
                opening_char = closing_to_opening_chars[char]
                if open_chars[-1] == opening_char:
                    open_chars.pop(-1)
                else:
                    corrupted_chars.append(char)
                    break

    scores = [illegal_char_score_values[char] for char in corrupted_chars]
    return sum(scores)


def part2():
    navigation_subsystem = parse_input()

    incomplete_lines_scores = []
    for line in navigation_subsystem:
        open_chars = []
        corrupted_line = False
        for char in line:
            if char in opening_chars:
                open_chars.append(char)
            else:
                opening_char = closing_to_opening_chars[char]
                if open_chars[-1] == opening_char:
                    open_chars.pop(-1)
                else:
                    corrupted_line = True
                    break

        if corrupted_line:
            continue

        incomplete_lines_score = 0
        for open_char in reversed(open_chars):
            closing_char = opening_to_closing_chars[open_char]
            char_score = autocomplete_char_score_values[closing_char]
            incomplete_lines_score = incomplete_lines_score * 5 + char_score
        incomplete_lines_scores.append(incomplete_lines_score)

    middle = int(len(incomplete_lines_scores)/2)
    score = sorted(incomplete_lines_scores)[middle]
    return score


def parse_input():
    navigation_subsystem = []
    with open("input.txt", "r") as input:
        for line in input:
            row = list(line.strip())
            navigation_subsystem.append(row)
    return navigation_subsystem


illegal_char_score_values = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

autocomplete_char_score_values = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

opening_chars = "([{<"
closing_chars = ")]}>"

opening_to_closing_chars = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}

closing_to_opening_chars = {v: k for k, v in opening_to_closing_chars.items()}


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
