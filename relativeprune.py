# -*- coding: utf-8 -*-
"""
Created on Thu Apr 3 13:06:49 2015

@author: Eeshan
"""

pt_file = "../data/en-hi/phrase-table-verysmall_normalized"
output = pt_file + '_relativepruned'
relativethreshold = 0.21

delim = " ||| "

pt = {}
# pt[source] = [ full-line ]
maxs = {}


f = open(pt_file, 'r')
for line in f:
    entries = line.split(delim)
    s = entries[0]
    probs = entries[2].split(' ')
    p = float(probs[2])
    if s not in pt:
        pt[s] = []
        maxs[s] = 0
    maxs[s] = max(p, maxs[s])
    pt[s].append([p, line])
f.close()


w = open(output, 'w')
keyset = pt.keys()
keyset.sort()

for s in keyset:
    m = maxs[s]
    for translations in pt[s]:
        p = translations[0]
        line = translations[1]
        if (p/m) < relativethreshold: 
            continue
        if line[len(line ) -1] != '\n': line = line + '\n'        
        w.write(line)

w.close()
        
print "Done"

    