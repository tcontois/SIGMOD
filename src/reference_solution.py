#!/usr/bin/env python
import sys

class Sigmod_Solver:

    def __init__(self):
        self.s_id = 1 # 0 is base
        self.transitions = {}
        self.outputs = set()
        self.longest = 0

    def add_ngram(self, ngram):
        prev_state = 0
        for i in range(len(ngram)):
            w = ngram[i]
            if prev_state not in self.transitions:
                ts = self.transitions[prev_state] = {}
            else:
                ts = self.transitions[prev_state]
            if w not in ts:
                ts[w] = self.s_id
                prev_state = self.s_id
                self.s_id += 1
            else:
                prev_state = ts[w]
        self.outputs.add(prev_state)
        if len(ngram) > self.longest:
            self.longest = len(ngram)

    def delete_ngram(self, ngram):
        prev_state = 0
        exists = True
        path = [0]
        for i in range(len(ngram)):
            w = ngram[i]
            if prev_state not in self.transitions:
                exists = False
                break
            ts = self.transitions[prev_state]
            if w in ts:
                prev_state = ts[w]
                path.append(prev_state)
            else:
                exists = False
                break
        if exists:
            self.outputs.discard(prev_state)
            if prev_state not in self.transitions: # prev state is path[-1]
                for x in range(2,len(path)+1):
                    i = path[-x]
                    w = ngram[-x+1]
                    t = self.transitions[i]
                    t.pop(w)
                    if not t:
                        self.transitions.pop(i)
                        prev_state = i
                        if prev_state in self.outputs:
                            break
                    else:
                        break

    def query(self, words):
        results = []
        found = set()
        buckets = [ [] for _ in range(self.longest)]
        cur_states = [(0,0)]
        b_index = 0
        for i in range(len(words)):
            w = words[i]
            for r in buckets[b_index]:
                results.append(r)
            buckets[b_index] = []
            new_states = [(0,0)]
            for x in cur_states:
                s = x[0]
                if s not in self.transitions:
                    continue
                ts = self.transitions[s]
                if w in ts:
                    new_id = ts[w]
                    new_states.append((new_id,x[1]+1))
                    if (new_id in self.outputs) and (new_id not in found):
                        place_index = b_index - (x[1])
                        if place_index < 0:
                            place_index += longest
                        buckets[place_index].append(" ".join(words[i-x[1]:i+1]))
                        found.add(new_id)
            cur_states = new_states
            b_index += 1
            if b_index == self.longest:
                b_index = 0
        for i in range(b_index, self.longest):
            for r in buckets[i]:
                results.append(r)
        for i in range(0, b_index):
            for r in buckets[i]:
                results.append(r)
        return results

def main():
    solver = Sigmod_Solver()
    initial_input = True
    while 1:
        words = sys.stdin.readline().split()
        if not words:
            break
        elif initial_input:
            if words[0] == "S":
                initial_input = False
                print('R')
                sys.stdout.flush()
            else:
                solver.add_ngram(words)
        else:
            if words[0] == "D":
                solver.delete_ngram(words[1:])
            elif words[0] == "A":
                solver.add_ngram(words[1:])
            elif words[0] == "Q":
                results = solver.query(words[1:])
                if not results:
                    print(-1)
                else:
                    print("|".join(results))
                sys.stdout.flush()
            elif words[0] == "F":
                continue

if __name__ == '__main__':
    main()