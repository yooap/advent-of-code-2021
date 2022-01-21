def part1():
    space1, space2 = parse_input()
    score1, score2 = 0, 0
    players_turn = 1
    dice = deterministic_dice()
    while max(score1, score2) < 1000:
        roll_resut = sum(dice.roll() for _ in range(3))
        if players_turn == 1:
            space1, score1 = move(space1, score1, roll_resut)
        else:
            space2, score2 = move(space2, score2, roll_resut)
        players_turn = switch_player(players_turn)
    return min(score1, score2) * dice.rolls


def part2():
    space1, space2 = parse_input()
    universe_storage = {((space1, 0), (space2, 0)): 1}
    player1_wins, player2_wins = 0, 0
    while len(universe_storage) > 0:
        updated_universe_storage = {}
        for universe, count in universe_storage.items():
            for i1 in range(1, 4):
                for i2 in range(1, 4):
                    for i3 in range(1, 4):
                        state1, state2 = universe
                        space1, score1 = state1
                        roll_resut = i1+i2+i3
                        space1, score1 = move(space1, score1, roll_resut)
                        if score1 >= 21:
                            player1_wins += count
                            continue

                        for j1 in range(1, 4):
                            for j2 in range(1, 4):
                                for j3 in range(1, 4):
                                    space2, score2 = state2
                                    roll_resut = j1+j2+j3
                                    space2, score2 = move(
                                        space2, score2, roll_resut)
                                    if score2 >= 21:
                                        player2_wins += count
                                        continue

                                    new_universe = (
                                        (space1, score1), (space2, score2))

                                    store_universe(
                                        updated_universe_storage, new_universe, count)

        universe_storage = updated_universe_storage

    return max(player1_wins, player2_wins)


def parse_input():
    start1, start2 = None, None
    with open("input.txt", "r") as input:
        start1 = read_line(input)
        start2 = read_line(input)
    return start1, start2


def read_line(input):
    return int(input.readline().strip().split(": ")[1])


def switch_player(players_turn):
    return 2 if players_turn == 1 else 1


def move(space, score, roll_resut):
    new_space = space + roll_resut
    if new_space > 10:
        new_space = new_space % 10
        if new_space == 0:
            new_space = 10
    new_score = score + new_space
    return new_space, new_score


class deterministic_dice:
    def __init__(self):
        self.value = 0
        self.rolls = 0

    def roll(self):
        self.rolls += 1
        self.value += 1
        if self.value > 100:
            self.value = 1
        return self.value


def store_universe(universe_storage, universe_state, count):
    universe_storage[universe_state] = count if universe_state not in universe_storage else universe_storage[universe_state] + count


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
