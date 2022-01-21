def part1():
    input = open("input.txt", "r")
    calculations = []
    for line in input:
        for i, bit in enumerate(line.strip()):
            assert bit in "01"
            if (len(calculations) < i+1):
                calculations.append(0)
            calculations[i] = calculations[i] + (1 if bit == "1" else -1)

    input.close()

    gamma, epsilon = "", ""
    for result in calculations:
        if result > 0:
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"

    result = int(gamma, 2) * int(epsilon, 2)
    return result


def part2():
    o2_gen, co2_scrub = None, None
    o2_gen_prefix, co2_scrub_prefix = "", ""
    while o2_gen == None or co2_scrub == None:
        o2_gen_prefix_hits, co2_scrub_prefix_hits = 0, 0
        o2_gen_bit_calc, co2_scrub_bit_calc = 0, 0
        o2_gen_candidate, co2_scrub_candidate = None, None

        with open("input.txt", "r") as input:
            for line_unstripped in input:
                line = line_unstripped.strip()
                if o2_gen == None and line.startswith(o2_gen_prefix):
                    o2_gen_prefix_hits += 1
                    o2_gen_candidate = line
                    bit = line[len(o2_gen_prefix):len(o2_gen_prefix)+1]
                    o2_gen_bit_calc += (1 if bit == "1" else -1)

                if co2_scrub == None and line.startswith(co2_scrub_prefix):
                    co2_scrub_prefix_hits += 1
                    co2_scrub_candidate = line
                    bit = line[len(co2_scrub_prefix):len(co2_scrub_prefix)+1]
                    co2_scrub_bit_calc += (1 if bit == "1" else -1)

        o2_gen_prefix += "0" if o2_gen_bit_calc < 0 else "1"
        co2_scrub_prefix += "0" if co2_scrub_bit_calc >= 0 else "1"

        if o2_gen_prefix_hits == 1:
            o2_gen = o2_gen_candidate
        if co2_scrub_prefix_hits == 1:
            co2_scrub = co2_scrub_candidate

    result = int(o2_gen, 2) * int(co2_scrub, 2)
    return result


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
