def part1():
    numbers = parse_input()
    result = None
    for number in numbers:
        if result == None:
            result = number
            continue

        result = sum_numbers(result, number)
    return calculate_magnitude(result)


def part2():
    numbers = parse_input()
    largest_magnitude = 0
    for number1 in numbers:
        for number2 in numbers:
            if number1 == number2:
                continue
            result = sum_numbers(number1, number2)
            magnitude = calculate_magnitude(result)
            if magnitude > largest_magnitude:
                largest_magnitude = magnitude
    return largest_magnitude


def parse_input():
    numbers = []
    with open("input.txt", "r") as input:
        for line in input:
            numbers.append(line.strip())
    return numbers


def sum_numbers(number1, number2):
    result = "[{},{}]".format(number1, number2)
    return reduce_number(result)


def reduce_number(number):
    number_before_iteration = None
    while number_before_iteration != number:
        number_before_iteration = number
        if (exlpodable_pair := find_exlpodable_pair(number)) != None:
            number = explode_pair(exlpodable_pair, number)
        elif (splitable_number := find_splitable_number(number)) != None:
            number = split_number(splitable_number, number)

    return number


def find_exlpodable_pair(number):
    exlpodable_pair = None
    open_brackets = 0
    index = 0
    for i, char in enumerate(number):
        if exlpodable_pair != None:
            exlpodable_pair = exlpodable_pair + char
            if char == "]":
                return (exlpodable_pair, index)
        else:
            if char == "[":
                open_brackets += 1
            elif char == "]":
                open_brackets -= 1

            if open_brackets == 5:
                index = i
                exlpodable_pair = "["


def explode_pair(pair_and_index, full_number):
    pair, initial_index = pair_and_index
    left_number, right_number = pair_to_numbers(pair)
    i = initial_index

    full_number = full_number[:i] + "0" + full_number[i+len(pair):]

    number_to_add_to = ""
    while i > 0:
        i -= 1
        char = full_number[i]
        if char.isnumeric():
            number_to_add_to = char + number_to_add_to
        elif len(number_to_add_to) > 0:
            i += 1
            new_number = int(number_to_add_to) + left_number
            full_number = full_number[:i] + \
                str(new_number) + full_number[i+len(number_to_add_to):]
            initial_index += len(str(new_number)) - len(number_to_add_to)
            break

    i = initial_index
    number_to_add_to = ""
    while i < len(full_number) - 1:
        i += 1
        char = full_number[i]
        if char.isnumeric():
            number_to_add_to = number_to_add_to + char
        elif len(number_to_add_to) > 0:
            i -= len(number_to_add_to)
            new_number = int(number_to_add_to) + right_number
            full_number = full_number[:i] + \
                str(new_number) + full_number[i+len(number_to_add_to):]
            break

    return full_number


def pair_to_numbers(pair):
    return [int(number)
            for number in pair[1:-1].split(",")]


def find_splitable_number(number):
    splitable_number = None
    for char in number:
        if char.isnumeric():
            if splitable_number == None:
                splitable_number = char
            else:
                splitable_number = splitable_number + char
                return splitable_number
        else:
            splitable_number = None


def split_number(split_number, full_number):
    left_number, right_number = (
        int(int(split_number) / 2), int((int(split_number) / 2) + .5))
    i = full_number.index(split_number)

    new_pair = "[{},{}]".format(left_number, right_number)
    return full_number[:i] + new_pair + full_number[i+2:]


def calculate_magnitude(number):
    pair = ""
    while "[" in number:
        for char in number:
            if char == "[":
                pair = "["
            else:
                pair = pair + char

            if char == "]":
                left, right = pair_to_numbers(pair)
                value = left*3 + right*2
                number = number.replace(pair, str(value))
                break
    return int(number)


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
