from collections import Counter

with open('input') as handle:
    template, rules = handle.read().split('\n\n')
    rules = dict(rule.split(' -> ') for rule in rules.split('\n') if rule)

def expand_template(template, rules, n_steps=5):
    for i in range(n_steps):
        template = ''.join([template[0]] + [rules.get(c+d, '') + d for c, d in zip(template[:-1], template[1:])])
    return template

all_bases = set(rules.values())
all_pairs = [c+d for c in all_bases for d in all_bases]
rewrite_rules = {tuple(k): expand_template(k, rules, 20) for k in all_pairs}

template = ''.join([rewrite_rules[c, d][:-1] for c, d in zip(template[:-1], template[1:])] + [template[-1]])

# We still need to take 20 steps. However, we can go to our solution directly.
count_rules = {k: Counter(v) for k, v in rewrite_rules.items()}
counts = {k: 0 for k in all_bases}
for c, d in zip(template[:-1], template[1:]):
    for k, v in count_rules[c, d].items():
        counts[k] += v
    counts[d] -= 1  # d will get counted twice
counts[d] += 1  # Except for the last one because there's no corresponding 'c'


print(max(counts.values()) - min(counts.values()))
