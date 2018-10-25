from termcolor import colored
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


def full_string(s):
    return ''.join([m for m in s if m not in ['(', ')']])


def parse_input(s):
    s = clean(s)
    opt_pattern = re.compile(r'\(([a-zàâçéèêëîïôûùüÿñæœ ]+)\)', flags=re.IGNORECASE)
    opts = opt_pattern.findall(s)
    if opts == None:
        opts = []
    all_words = list(filter(lambda x: x != '', opt_pattern.split(s)))
    opts = [clean(x) for x in opts]
    all_words = [clean(x) for x in all_words]
    ans = possible_answers(all_words, opts) 
    ans.sort(reverse=True)
    return ans


def merge_dict_sets(dest, src):
    for k, v_list in src.items():
        if k in dest:
            dest[k] = dest[k].union(set(v_list))
        else:
            dest[k] = set(v_list)
    return dest


class CardSet:
    front = 0
    back = 1
    
    def __init__(self, names):
        self.front_name, self.back_name = clean(names).split(':')
        self.edges = []
        self.accepted = {}
        self.fronts = []
        self.backs = []
        self.tmap = {}
        self._i = 0

    def add_card(self, input_str):
        f, b = map(clean, input_str.split(':'))
        # fr, ba map full_string -> [accepted_strings]
        fr = self._make_dict(f)
        ba = self._make_dict(b)
        # add keys to list of front, back terms if not already present
        self.fronts = list(set(self.fronts).union(set(fr.keys())))
        self.backs = list(set(self.backs).union(set(ba.keys())))

        # update graph
        for fr_k in fr.keys():
            for ba_k in ba.keys():
                i = self.tmap[fr_k]
                j = self.tmap[ba_k]
                self.edges[i].append(j)
                self.edges[j].append(i)

        # replace keys with mapped integers 
        fr = {self.tmap[k]:v for k, v in fr.items()}
        ba = {self.tmap[k]:v for k, v in ba.items()}

        self.accepted = merge_dict_sets(self.accepted, fr)
        self.accepted = merge_dict_sets(self.accepted, ba)

    def match(self, question, answer):
        for u in self.edges[self.tmap[question]]:
            if answer in self.accepted[u]:
                return True
        return False

    def answers(self, question):
        return [self.tmap[i] for i in self.edges[self.tmap[question]]]

    def _make_dict(self, str_in):
        d = {} # unique id string -> all accepted alternatives
        for x in str_in.split(','):
            s = full_string(x)
            if s not in self.tmap.keys():
                self.tmap[s] = self._i
                self.tmap[self._i] = s
                self.edges.append([])
                self._i += 1
            d[s] = parse_input(x)
        return d


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print('Error: must provide flashcard file')
    else:
        fc_file = open(sys.argv[1], 'r')
        fc_file.seek(0)
        cards = CardSet(fc_file.readline())
        
        for line in fc_file.readlines():
            cards.add_card(line)

        while True:
            print()
            q = ''
            s = randint(0, 1)
            if s:
                q = cards.fronts[randint(0, len(cards.fronts)-1)]
            else:
                q = cards.backs[randint(0, len(cards.backs)-1)]
            print(q, end=': ')
            ans = input()
            if ans == 'q!':
                break
            if cards.match(q, ans):
                print(colored('Correct!', 'green'), end = ' ')
            else:
                print(colored('Wrong!', 'red'), end = ' ')
            print(', '.join(cards.answers(q)))
