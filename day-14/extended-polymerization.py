def part1():
    polymer_result, insertions_pairs = parse_input()
    for i in range(10):
        insertions_this_step = []
        for insertions_pair in insertions_pairs:
            char_pair = insertions_pair[0]
            if char_pair in polymer_result:
                indexes = find_indexes(polymer_result, char_pair)
                for index in indexes:
                    insertion = (index, insertions_pair[1])
                    insertions_this_step.append(insertion)
        insertions_this_step.sort(
            key=lambda insertion: insertion[0], reverse=True)
        for insertion in insertions_this_step:
            index = insertion[0]
            polymer_result = polymer_result[:index] + \
                insertion[1] + polymer_result[index:]
    char_counts = get_char_counts(polymer_result)
    return char_counts[-1] - char_counts[0]


def part2():
    polymer_template, insertions_pairs = parse_input()

    pairs = {}
    for i in range(len(polymer_template) - 1):
        update_pairs_map(pairs, polymer_template[i:i+2], 1)
    start_char, end_char = polymer_template[0], polymer_template[-1]

    for i in range(40):
        updated_pairs = {}
        for insertions_pair in insertions_pairs:
            char_pair = insertions_pair[0]
            if char_pair in pairs:
                count = pairs[char_pair]
                insertion_char = insertions_pair[1]
                new_pair_1 = char_pair[0] + insertion_char
                new_pair_2 = insertion_char + char_pair[1]
                update_pairs_map(updated_pairs, new_pair_1, count)
                update_pairs_map(updated_pairs, new_pair_2, count)
                del pairs[char_pair]
        for remaning_pair, count in pairs.items():
            update_pairs_map(updated_pairs, remaning_pair, count)
        pairs = updated_pairs
    char_counts = get_char_counts_from_map(pairs, start_char, end_char)
    return char_counts[-1] - char_counts[0]


def parse_input():
    template, insertions_pairs = "", list()
    with open("input.txt", "r") as input:
        for unstripped_line in input:
            line = unstripped_line.strip()
            if line:
                if "->" in line:
                    char_pair, insertion_char = line.split(" -> ")
                    insertions_pairs.append((char_pair, insertion_char))
                else:
                    template = line

    return template, insertions_pairs


def find_indexes(polymer_result, char_pair):
    indexes = [polymer_result.index(char_pair) + 1]
    last_index = 0
    lookup_string = polymer_result
    while last_index != indexes[-1]:
        last_index = indexes[-1]
        lookup_string = polymer_result[last_index:]
        if char_pair in lookup_string:
            index = lookup_string.index(char_pair) + last_index + 1
            indexes.append(index)
    return indexes


def get_char_counts(polymer_result):
    counts = []
    unique_chars = set(polymer_result)
    for char in unique_chars:
        count = polymer_result.count(char)
        counts.append(count)
    return sorted(counts)


def update_pairs_map(pairs, pair, count):
    if pair in pairs:
        pairs[pair] = pairs[pair] + count
    else:
        pairs[pair] = count


def get_char_counts_from_map(pairs, start_char, end_char):
    counts_map = {}
    for pair, count in pairs.items():
        for char in pair:
            if char in counts_map:
                counts_map[char] = counts_map[char] + count
            else:
                counts_map[char] = count
    
    counts_map[start_char] = counts_map[start_char] + 1
    counts_map[end_char] = counts_map[end_char] + 1
    return sorted([int(count/2) for count in counts_map.values()])


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
