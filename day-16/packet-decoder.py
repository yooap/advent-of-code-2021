def part1():
    hex_line = parse_input()
    binary_line = ""
    for hex_char in hex_line:
        binary_value = str(bin(int(hex_char, 16)))[2:].zfill(4)
        binary_line = binary_line + binary_value

    packet, _ = read_packet(binary_line)
    return add_up_version_numbers(packet)


def read_packet(binary_packet):
    packet = {}
    version = int(binary_packet[:3], 2)
    type = int(binary_packet[3:6], 2)

    packet["version"] = version
    packet["type"] = type

    end_index = None
    if type == 4:  # literal value
        index = 6
        value = ""
        value_end = False
        while not value_end:
            value_part = binary_packet[index:index+5]
            index += 5
            value_end = int(value_part[0]) == 0
            value = value + value_part[1:5]
        packet["value"] = int(value, 2)
        end_index = index
    else:  # operator
        length_type = int(binary_packet[6])
        packet["sub_packets"] = []
        if length_type == 0:  # total length in bits
            total_length = int(binary_packet[7:22], 2)
            end_index = 22+total_length
            sub_packet_start_index = 22
            while sub_packet_start_index < end_index:
                sub_packet, sub_packet_end_index = read_packet(
                    binary_packet[sub_packet_start_index:end_index])
                packet["sub_packets"].append(sub_packet)
                sub_packet_start_index += sub_packet_end_index
        else:  # number of sub-packets immediately contained
            packet_count = int(binary_packet[7:18], 2)
            sub_packet_start_index = 18
            for i in range(packet_count):
                sub_packet, sub_packet_end_index = read_packet(
                    binary_packet[sub_packet_start_index:])
                packet["sub_packets"].append(sub_packet)
                sub_packet_start_index += sub_packet_end_index
            end_index = sub_packet_start_index

    return packet, end_index


def add_up_version_numbers(packet):
    sum = packet["version"]
    if "sub_packets" in packet:
        sub_packets = packet["sub_packets"]
        for sub_packet in sub_packets:
            sum += add_up_version_numbers(sub_packet)
    return sum


def part2():
    hex_line = parse_input()
    binary_line = ""
    for hex_char in hex_line:
        binary_value = str(bin(int(hex_char, 16)))[2:].zfill(4)
        binary_line = binary_line + binary_value

    packet, _ = read_packet(binary_line)
    return calculate(packet)


def calculate(packet):
    type = packet["type"]
    return {
        0: lambda packet: sum(calculate(packet) for packet in packet["sub_packets"]),
        1: lambda packet: prod([calculate(packet) for packet in packet["sub_packets"]]),
        2: lambda packet: min(calculate(packet) for packet in packet["sub_packets"]),
        3: lambda packet: max(calculate(packet) for packet in packet["sub_packets"]),
        4: lambda packet: packet["value"],
        5: lambda packet: 1 if calculate(packet["sub_packets"][0]) > calculate(packet["sub_packets"][1]) else 0,
        6: lambda packet: 1 if calculate(packet["sub_packets"][0]) < calculate(packet["sub_packets"][1]) else 0,
        7: lambda packet: 1 if calculate(packet["sub_packets"][0]) == calculate(packet["sub_packets"][1]) else 0
    }[type](packet)


def prod(values):
    result = 1
    for value in values:
        result = result * value
    return result


def parse_input():
    hex_line = []
    with open("input.txt", "r") as input:
        hex_line = input.readline().strip()
    return hex_line


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
