from random import randint
import itertools as it
import sys
import re


def clean(s):
    return s.strip().rstrip()


def possible_answers(words, opt):
    if opt == []:
        return [' '.join(words)]
    ans = []
    req_ind = []
    opt_ind = []
    i = 0
    j = 0
    while j < len(opt):
        if words[i] == opt[j]:
            opt_ind.append(i)
            j += 1
        else:
            req_ind.append(i)
        i += 1
    while i < len(words):
        req_ind.append(i)
        i += 1

    comb_iter = (it.combinations(opt_ind, n) for n in range(len(opt_ind)+1))
    combs = list(it.chain.from_iterable(comb_iter))
    combs = [sorted(req_ind + list(x)) for x in combs]

    for c in combs:
        ans.append(' '.join([words[x] for x in c]))
    return ans


def parse_input(s):
    s = clean(s)
    opt_pattern = re.compile(r'\(([a-zàâçéèêëîïôûùüÿñæœ]+)\)', flags=re.IGNORECASE)
    for x in s.split(','):
        opts = opt_pattern.findall(x)
        if opts == None:
            opts = []
        all_words = list(filter(lambda x: x != '', opt_pattern.split(x)))
        opts = [clean(s) for s in opts]
        all_words = [clean(s) for s in all_words]
    return possible_answers(all_words, opts) 


class Card:
    front = 0
    back = 1

    def __init__(self, input_str):
        f, b = input_str.split(':')
        self.ans = [parse_input(f), parse_input(b)]

    def match(self, side, s):
        return s in self.ans[side]


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print('Must provide flashcard file')
    else:
        fc_file = open(sys.argv[1], 'r')
        fc_file.seek(0)
        front, back = fc_file.readline().split(':')
        cards = []
        for line in fc_file.readlines():
            cards.append(Card(line))

        while True:
            print()
            card = cards[randint(0, len(cards)-1)]
            s = randint(0, 1)
            print(card.ans[s][0], end=': ')
            ans = input()
            if card.match(not s, ans):
                print("Correct!")
            else:
                print("Wrong - " + card.ans[not s][0])
