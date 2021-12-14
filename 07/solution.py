with open('input') as handle:
    data = [int(x) for x in handle.read().strip().split(',')]

counts = [sum(x == i for x in data) for i in range(max(data)+1)]

# Score for part 2: step 1 has cost 1, step 2 cost 2, i.e.
# where n = abs(x-loc): 1 + 2 + 3 + ... + n
# gauss: 0.5*n*(n+1)
def score(loc):
    weights = [abs(x-loc) for x in range(len(counts))]
    weights = [0.5*n*(n+1) for n in weights]  
    return sum(c*w for c, w in zip(counts, weights))

start = 0
end = len(counts) 
while end-start > 1: 
    middle = int((start+end) / 2)
    if score(start) <= score(end):
        end = middle
    else:
        start = middle

print(start, score(start), end, score(end), middle, score(middle))


