def part1():
    draws, boards, board_hits = read_input()

    draw = None
    winning_board_idx = None
    while winning_board_idx == None:
        draw = draws.pop(0)
        winning_board_idx = check_for_bingo(boards, board_hits, draw)

    unmarked_score = sum_unmarked_number_score(
        boards, board_hits, winning_board_idx)
    return unmarked_score * draw


def read_input():
    draws = None
    boards = []
    board_hits = []
    with open("input.txt", "r") as input:
        for line_unstripped in input:
            line = line_unstripped.strip()
            if draws == None:
                draws = [int(draw) for draw in line.split(",")]
                continue

            if len(line) == 0:
                # start new board
                boards.append([])
                board_hits.append([])
                continue

            current_board = boards[-1]
            current_board_hits = board_hits[-1]
            row = [int(number) for number in line.split()]
            current_board.append(row)
            current_board_hits.append([False] * len(row))

    return draws, boards, board_hits


def check_for_bingo(boards, board_hits, draw):
    for board_idx, board in enumerate(boards):
        for row_idx, row in enumerate(board):
            for column_idx, number in enumerate(row):
                if number != draw:
                    continue

                board_hits[board_idx][row_idx][column_idx] = True
                row_bingo = all(board_hits[board_idx][row_idx])
                column_bingo = all([row[column_idx]
                                   for row in board_hits[board_idx]])
                if row_bingo or column_bingo:
                    return board_idx


def sum_unmarked_number_score(boards, board_hits, board_idx):
    unmarked_score = 0
    for row_idx, row in enumerate(board_hits[board_idx]):
        for column_idx, hit in enumerate(row):
            if not hit:
                unmarked_score += boards[board_idx][row_idx][column_idx]
    return unmarked_score


def part2():
    draws, boards, board_hits = read_input()

    draw = None
    losing_board_idx = None
    while losing_board_idx == None:
        draw = draws.pop(0)
        while True:
            winning_board_idx = check_for_bingo(boards, board_hits, draw)
            if winning_board_idx == None:
                break
            else:
                if len(boards) == 1:
                    losing_board_idx = winning_board_idx
                    break
                else:
                    del boards[winning_board_idx]
                    del board_hits[winning_board_idx]

    unmarked_score = sum_unmarked_number_score(boards, board_hits, 0)
    return unmarked_score * draw


if __name__ == "__main__":
    print("Part 1: " + str(part1()))
    print("Part 2: " + str(part2()))
