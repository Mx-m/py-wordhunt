import random
import time


def preprocess_words(filename, max_length, grid):
    possible_words = []
    starting_letters = list(cell for row in grid for cell in row)
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.upper().strip()
            if len(word) <= max_length:
                for char in list(word):
                    if char in starting_letters:
                        if word.index(char) == len(word) - 1:
                            possible_words.append(word)
                    else:
                        break
    return possible_words


def longest_word(gb):
    max_length = len(gb) * len(gb[0])  # max possible length of a word in the grid
    possible_words = preprocess_words('english.txt', max_length, gb)
    longest_word = ''
    for word in possible_words:
        if len(word) <= len(longest_word):
            continue  # skip if the word is not longer than the current longest word

        check = check_ans(gb, word, [])
        if check[0]:
            longest_word = word
            if len(longest_word) == max_length:
                break  # exit if longest possible word found

    return longest_word


def init_gameboard():
    def generate_grid(size):
        # letter frequency list for English
        letter_pool = "EEEEAAAOOIINNRRTTLLSSUUDDGGHHCMMFFYYBBVVKKWWXZQJ"
        grid = []
        for _ in range(size):
            row = [random.choice(letter_pool) for _ in range(size)]
            grid.append(row)
        # insert a word for playability later...
        return grid

    gb = generate_grid(4)
    return gb


def update_board(gb, score, time):
    time = int(time)
    for row in gb:
        print('|', ' '.join(row), '|')
    if time < 0:
        time = 0
    padded_score = str(score).rjust(5)
    padded_time = str(time).ljust(4)
    print(f'⌈{padded_time}{padded_score}⌉')


def isword(word):
    word = word.lower()
    with open('english.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if word == line:
                return True
        return False


def check_ans(gb, ans, ansls):
    ans = ans.upper()
    ans_arr = list(ans)
    rows, cols = len(gb), len(gb[0])
    word_len = len(ans_arr)

    def dfs(x, y, index):
        if index == word_len:
            return True
        if x < 0 or x >= rows or y < 0 or y >= cols or gb[x][y] != ans_arr[index]:
            return False

        # mark the cell as visited
        temp, gb[x][y] = gb[x][y], '#'

        # define possible directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        # explore all directions
        found = any(dfs(x + dx, y + dy, index + 1) for dx, dy in directions)

        # restore cell value
        gb[x][y] = temp

        return found

    # find word in gb
    if ans not in ansls:
        if word_len >= 3:
            if isword(ans):
                for i in range(rows):
                    for j in range(cols):
                        if dfs(i, j, 0):
                            return True, ''
                return False, 'not on board'
            return False, 'not a word'
        return False, 'word too short'
    return False, 'already guessed'


if __name__ == '__main__':
    game_over = False
    gb = init_gameboard()
    score = 0
    score_dict = {3: 100, 4: 400, 5: 800, 6: 1400, 7: 1800, 8: 2200}
    ansls = []

    # init timer, if just enter then defaults to 60 seconds
    timer = input('how much time(seconds): ')
    if timer == '':
        timer = -1
    # game start
    gamestart = input('press enter to start')
    # timer = 60

    # prints board
    update_board(gb, score, timer)
    # starts timer
    start = time.time()
    # init round time
    if timer == 0:
        round_time = time.time() + 100
    elif timer == -1:
        round_time = 60
    else:
        round_time = int(timer)
    # starts game condition
    while (time.time() - start) < round_time and not game_over:
        ans = input('word: ')
        if ans == 'quit()':
            game_over = True
        check, status = check_ans(gb, ans, ansls)
        if check:
            ansls.append(ans.upper())
            length = len(list(ans))
            if length > 8:
                round_score = 2200 + ((length - 8) * 400)
            else:
                round_score = score_dict[length]
            score += round_score
        else:
            print(status)
        timeleft = round_time - int(time.time() - start)
        update_board(gb, score, timeleft)
    if score >= 124600:
        print('you\'re better than jay\'s brother!')
    print('words:', len(ansls))
    print('words found:', ansls)
    longest_word = longest_word(gb)
    print('longest word possible:', longest_word)
    print('\nfinal score:', score)
