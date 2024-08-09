import random

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


def update_board(gb, score):
    for row in gb:
        print('|', ' '.join(row), '|')
    print('⌈      ', score, '⌉')


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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game_over = False
    gb = init_gameboard()
    score = 0
    score_dict = {3: 100, 4: 400, 5: 800, 6: 1400, 7: 1800, 8: 2200}
    ansls = []
    update_board(gb, score)
    while not game_over:
        ans = input('word: ')
        check, status = check_ans(gb, ans, ansls)
        if check:
            ansls.append(ans.upper())
            length = len(list(ans))
            if length > 8:
                round_score = 2200 + ((length-8)*400)
            else:
                round_score = score_dict[length]
            score += round_score
        else:
            print(status)
        update_board(gb, score)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
