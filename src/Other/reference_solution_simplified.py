import sys

class Sigmod_Solver:

    def __init__(self):
        self.s_id = 1 # 0 is base
        self.transitions = {}
        self.outputs = set()

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

    def delete_ngram(self, ngram):
        prev_state = 0
        exists = True
        for i in range(len(ngram)):
            w = ngram[i]
            if prev_state not in self.transitions:
                exists = False
                break
            ts = self.transitions[prev_state]
            if w in ts:
                prev_state = ts[w]
            else:
                exists = False
                break
        if exists:
            self.outputs.discard(prev_state)

    def query(self, words):
        results = []
        found = set()
        cur_states = [0]
        for i in range(len(words)):
            w = words[i]
            new_states = [0]
            for s in cur_states:
                if s not in self.transitions:
                    continue
                ts = self.transitions[s]
                if w in ts:
                    new_id = ts[w]
                    new_states.append((new_id,x[1]+1))
                    if (new_id in self.outputs) and (new_id not in found):
                        results.append(" ".join(words[i])) # just last word for now because simplfied
                        found.add(new_id)
            cur_states = new_states
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