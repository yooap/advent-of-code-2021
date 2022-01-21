def part1():
    output_values = []
    with open("input.txt", "r") as input:
        for line in input:
            output_values_for_line = line.split("|")[1].strip().split()
            output_values.extend(output_values_for_line)
    output_value_lengths = [len(value) for value in output_values]

    relevant_lengths = [2, 4, 3, 7]  # 1, 4, 7, 8
    result = len(
        [length for length in output_value_lengths if length in relevant_lengths])

    return result


def part2():
    lines = []
    with open("input.txt", "r") as input:
        for line in input:
            signals, outputs = line.strip().split("|")
            line = (signals.split(), outputs.split())
            lines.append(line)

    output_values = []
    for line in lines:
        signals = line[0]
        decyphered_dict = decypher(signals)
        outputs = line[1]
        decyphered_value = ""
        for output_value in outputs:
            for value, signal in decyphered_dict.items():
                if set(output_value) == set(signal):
                    decyphered_value += str(value)
                    break
        output_values.append(int(decyphered_value))

    return sum(output_values)


def decypher(signals):
    decyphered_dict = {}
    for signal in signals:  # find 1, 4, 7, 8 first
        signal_length = len(signal)
        if signal_length == 2:  # 1
            decyphered_dict[1] = signal
        elif signal_length == 4:  # 4
            decyphered_dict[4] = signal
        elif signal_length == 3:  # 7
            decyphered_dict[7] = signal
        elif signal_length == 7:  # 8
            decyphered_dict[8] = signal

    difference_4_and_7 = set(decyphered_dict[4]) - set(decyphered_dict[7])
    for signal in signals:
        signal_length = len(signal)
        if signal_length == 5:  # 2,3,5
            if all(char in signal for char in decyphered_dict[1]):  # 3
                decyphered_dict[3] = signal
            elif all(char in signal for char in difference_4_and_7):  # 5
                decyphered_dict[5] = signal
            else:  # 2
                decyphered_dict[2] = signal

        elif signal_length == 6:  # 0,6,9
            if all(char in signal for char in decyphered_dict[4]):  # 9
                decyphered_dict[9] = signal
            elif all(char in signal for char in decyphered_dict[1]):  # 0
                decyphered_dict[0] = signal
            else:  # 6
                decyphered_dict[6] = signal

    return decyphered_dict


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
