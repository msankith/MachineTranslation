# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 13:06:49 2015

@author: Eeshan
"""

pt_file = "../data/en-hi/phrase-table-verysmall"
output = pt_file + '_normalized'
delim = " ||| "

pt = {}
# pt[source] = [ [part 1, prob, part2],  [], [] ]

sums = {}

f = open(pt_file, 'r')
for line in f:
    entries = line.split(delim)
    s = entries[0]
    probs = entries[2].split(' ')
    p = float(probs[2])
    part1 = entries[0] + delim + entries[1] + delim + probs[0] + ' ' + probs[1] + ' '
    part2 =  ' ' + probs[3] + ' ' + probs[4] + delim + entries[3] + delim + entries [4]
    if s not in pt:
        pt[s] = []
        sums[s] = 0
    
    sums[s]+= p
    pt[s].append([part1, p, part2])

f.close()


w = open(output, 'w')
keyset = pt.keys()
keyset.sort()

for s in keyset:
    total = sums[s]
    for translations in pt[s]:
        line = translations[0]+ str(translations[1]/total) + translations[2]
        if line[len(line ) -1] != '\n': line = line + '\n'        
        w.write(line)

w.close()
        
print "Done"

    