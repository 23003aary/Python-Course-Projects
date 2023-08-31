
"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 30, 2021
"""


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "] * sz)
    return board


def is_empty(board):
    ''' Check if all elements of list of lists 'board' are " " '''
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != ' ':
                return False
    return True


def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    ''' Returns whether a sequence is OPEN, SEMIOPEN or Closed, Checking from the end position of the
    sequence'''

    n, k = len(board), len(board[0])

    start_x = x_end - (length - 1) * d_x
    start_y = y_end - (length - 1) * d_y

    open_from_start = False
    if 0 <= start_x - d_x < k and 0 <= start_y - d_y < n:
        square = board[start_y - d_y][start_x - d_x]
        if square == ' ':
            open_from_start = True

    open_from_end = False
    if 0 <= x_end + d_x < k and 0 <= y_end + d_y < n:
        square = board[y_end + d_y][x_end + d_x]
        if square == ' ':
            open_from_end = True

    if open_from_start and open_from_end:
        return "OPEN"
    if open_from_start or open_from_end:
        return "SEMIOPEN"
    else:
        return "CLOSED"


def check_run(board, y_start, x_start, d_y, d_x, col):
    ''' Checks the length of a sequence given a direction'''
    cur_length = 0
    if board[y_start][x_start] != col:
        return 0

    while board[y_start][x_start] == col:
        cur_length += 1
        y_start = y_start + d_y
        x_start = x_start + d_x
        if y_start == 8 or x_start == 8 or y_start < 0 or x_start < 0:
            break
    return cur_length


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    '''Checks whether a sequence of a length, in a directional row is OPEN or SEMIOPEN'''
    open_seq_count = 0
    semi_open_seq_count = 0

    n, k = len(board), len(board[0])

    seq_starts = []
    y, x = y_start, x_start

    start = None
    in_sequence = True
    while 0 <= y < n and 0 <= x < k:
        square = board[y][x]
        if square != col and start:
            seq_starts.append(start)
            start = None
        if square == col and not start:
            start = y, x
        y += d_y
        x += d_x
    if start:
        seq_starts.append(start)

    for y_start, x_start in seq_starts:
        seq_length = check_run(board, y_start, x_start, d_y, d_x, col)
        if length != seq_length:
            continue
        y_end, x_end = y_start + (length - 1) * d_y, x_start + (length - 1) * d_x
        status = is_bounded(board, y_end, x_end, length, d_y, d_x)
        if status == "SEMIOPEN":
            semi_open_seq_count += 1
        elif status == "OPEN":
            open_seq_count += 1

    return open_seq_count, semi_open_seq_count


def detect_rows(board, col, length):
    # CHANGE ME
    '''Return's avalaible open sequence and semi open sequences on the board'''

    open_seq_count, semi_open_seq_count = 0, 0

    n, k = len(board), len(board[0])
    for i in range(n):

        y = detect_row(board, col, i, 0, length, 0, 1)
        semi_open_seq_count += y[1]
        open_seq_count += y[0]

        # check coloumns d_x = 0 d_y = 1
        x = detect_row(board, col, 0, i, length, 1, 0)
        semi_open_seq_count += x[1]
        open_seq_count += x[0]

        # check diagonal top left down

        if i == 0:
            for j in range(k):
                z_1 = detect_row(board, col, i, j, length, 1, 1)
                semi_open_seq_count += z_1[1]
                open_seq_count += z_1[0]
        if i != 0:
            z1 = detect_row(board, col, i, 0, length, 1, 1)
            semi_open_seq_count += z1[1]
            open_seq_count += z1[0]

            # check diagonal top right down

        if i == 0:
            for j in range(k):
                z2 = detect_row(board, col, i, j, length, 1, -1)
                semi_open_seq_count += z2[1]
                open_seq_count += z2[0]

        if i != 0:
            z2 = detect_row(board, col, i, k - 1, length, 1, -1)
            semi_open_seq_count += z2[1]
            open_seq_count += z2[0]

    return open_seq_count, semi_open_seq_count


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i)
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))


def search_max(board):
    '''Returns coordinate of best possible move to increase score'''
    best = None
    best_y, best_x = None, None
    n, k = len(board), len(board[0])
    for y in range(n):
        for x in range(k):
            if board[y][x] != ' ':
                continue
            board[y][x] = 'b'
            cur_score = score(board)
            if best is None or cur_score > best:
                best = cur_score
                best_y, best_x = y, x
            board[y][x] = ' '
    return best_y, best_x


def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)

    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4]) +
            500 * open_b[4] +
            50 * semi_open_b[4] +
            -100 * open_w[3] +
            -30 * semi_open_w[3] +
            50 * open_b[3] +
            10 * semi_open_b[3] +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    '''Checks wether a sequence on the board is a winning sequence'''
    return_statement = {'w': 'White won', 'b': 'Black won'}
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    n, k = len(board), len(board[0])
    sequences = {}
    for start_y in range(n):
        for start_x in range(k):
            for (d_y, d_x) in directions:
                col = board[start_y][start_x]
                if col == ' ':
                    continue
                length = check_run(
                    board, start_y, start_x, d_y, d_x, col)
                sequences[length] = sequences.get(length, [])
                sequences[length].append((start_y, start_x, d_y, d_x))
    # invalid_sequences = set()
    # for length in sorted(list(sequences.keys()), reverse=True):
    #     if length == 5:
    #         break
    #     for seq in sequences[length]:
    #         start_y, start_x, d_y, d_x = seq
    #         for i in range(length):
    #             invalid_sequences.add((start_y + d_y * i, start_x + d_x * i))
    if 5 in sequences:
        for seq in sequences[5]:
            start_y, start_x, d_y, d_x = seq
            if 0 <= start_y - d_y < n and 0 <= start_x - d_x < k:
                square = board[start_y - d_y][start_x - d_x]
                if square == board[start_y][start_x]:
                    continue
            if 0 <= start_y + 5 * d_y < n and 0 <= start_x + 5 * d_x < k:
                square = board[start_y + 5 * d_y][start_x + 5 * d_x]
                if square == board[start_y][start_x]:
                    continue
            return return_statement[board[start_y][start_x]]

    if all(board[y][x] != ' ' for y in range(n) for x in range(k)):
        return "Draw"

    return "Continue playing"


def print_board(board):
    s = "*"
    for i in range(len(board[0]) - 1):
        s += str(i % 10) + "|"
    s += str((len(board[0]) - 1) % 10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i % 10)
        for j in range(len(board[0]) - 1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0]) - 1])

        s += "*\n"
    s += (len(board[0]) * 2 + 1) * "*"

    print(s)


def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        # analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res