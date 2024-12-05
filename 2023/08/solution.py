from collections import defaultdict
from copy import deepcopy

with open('input') as handle:
    data = [line.strip().split('|') for line in handle.readlines()]
    data = [([''.join(sorted(item)) for item in first.split()], [''.join(sorted(item)) for item in second.split()])
            for first, second in data]

patterns = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']

def s_to_n(s):
    return {2: 1, 3: 7, 4: 4, 7: 8}.get(len(s), None)

def reduce(candidates):
    old_candidates = None
    while old_candidates != candidates:
        old_candidates = deepcopy(candidates)

        sure = {k: v for k, v in candidates.items() if len(v) == 1}
        if any(sure):
            to_remove = {c for known in sure.values() for c in known}
            skip = sure.keys()
            for char in candidates.keys():
                if char in skip: continue
                candidates[char] -= to_remove
                
        pairs = defaultdict(list)
        for k, v in candidates.items(): pairs[''.join(sorted(v))].append(k)
        pairs = {k: v for k, v in pairs.items() if len(k) == len(v) and len(k) > 1}

        if any(pairs):
            to_remove = {c for pair in pairs.keys() for c in pair}
            skip = {c for pair in pairs.values() for c in pair}
            for char in candidates.keys():
                if char in skip: continue
                candidates[char] -= to_remove

    return candidates

def get_all_options(candidates):
    if not any(len(v) > 1 for v in candidates.values()): return [candidates]

    all_options = []
    choice_at = [k for k, v in candidates.items() if len(v) > 1][0]
    for choice in candidates[choice_at]:
        these_candidates = deepcopy(candidates)
        these_candidates[choice_at] = {choice}
        all_options.extend(get_all_options(reduce(these_candidates)))
    return [{k: list(v)[0] for k, v in opt.items()} for opt in all_options]

def is_valid(mapping, entry_input):
    return all(''.join(sorted(mapping[c] for c in entry)) in patterns for entry in entry_input)

def get_mapping(entry_input):
    rosetta = {s: patterns[k] for s in entry_input if (k := s_to_n(s)) in (1, 4, 7, 8)}
    candidates = {c: set('abcdefg') for c in 'abcdefg'}

    for char in 'abcdefg':
        for k, v in rosetta.items():
            if char in k: candidates[char] &= set(v)

    candidates = reduce(candidates)
    return [opt for opt in get_all_options(candidates) if is_valid(opt, entry_input)][0]

def translate(entry_input, entry_output):
    mapping = get_mapping(entry_input)
    output_value = sum(10**(3-i) * patterns.index(''.join(sorted(mapping[c] for c in digit))) for i, digit in enumerate(entry_output))
    return output_value

print(sum(translate(i, o) for i, o in data))
