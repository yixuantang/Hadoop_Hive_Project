#!/usr/bin/env python
import sys

res = {}
for line in sys.stdin:
    word, count = line.split('\t')
    count = int(count)

    if (res is None) or (word not in res.keys()):
        res[word] = count
    else:
        res[word] += 1

for word in res.keys():
    print ('{0}\t{1}'.format(word, res[word]))
