# -*- coding: utf-8 -*-
"""
Created on Wed Apr 08 15:36:38 2015

@author: Eeshan
"""
suffix = "-100k"
file_pt_en_hi = "../data/en-hi/phrase-table" + suffix
file_hi_mr = "../data/hi-mr/phrase-table" + suffix
file_en_mr = "../output/en-mr-phrase-table-phase1" + suffix
delim = " ||| "


def combinealignments(alignsp, alignpt):
    splist = alignsp.split(" ")
    ptlist = alignpt.split(" ")
    ps = {}
    for pair in [y.split("-") for y in splist]:
        s = pair[0]
        p = pair[1]
        if not p in ps:
            ps[p] = []
        ps[p].append(s)
        
    pt = {}
    for pair in [y.split("-") for y in ptlist]:
        p = pair[0]
        t = pair[1]
        if not p in pt:
            pt[p] = []
        pt[p].append(t)
    alignments = []
    for p in ps:
        if p in pt:
            for s in ps[p]:
                for t in pt[p]:
                    alignments.append(s + "-" + t)
    return alignments
    


# Load En-Hi
pt_en_hi = {}

f_en_hi = open(file_pt_en_hi, 'r')
for line  in f_en_hi:
    row = line.split(delim)
    en = row[0]
    hi = row[1]
    prob_numbers = row[2]
    alignments = row [3]
    counts = row[4]
    probs = [float (x) for x in (prob_numbers.split(' '))]
    if not en in pt_en_hi:
        pt_en_hi[en] = {}
    pt_en_hi[en][hi] = probs + [alignments] + [counts]

f_en_hi.close()
#print pt_en_hi


# Load hi-mr
pt_hi_mr = {}

f_hi_mr = open(file_hi_mr, 'r')
for line  in f_hi_mr:
    row = line.split(' ||| ')
    hi = row[0]
    mr = row[1]
    prob_numbers = row[2]
    alignments = row [3]
    counts = row[4]
    probs = [float (x) for x in (prob_numbers.split(' '))]
    if not hi in pt_hi_mr:
        pt_hi_mr[hi] = {}
    pt_hi_mr[hi][mr] = probs + [alignments] + [counts]
f_hi_mr.close()
#print pt_hi_mr

#verification:
#for a in pt_hi_mr:
#    sum = 0
#    for b in pt_hi_mr[a]:
#        sum+=pt_hi_mr[a][b][2]
#    print a, sum




###########################################
####### Combine Translation tables  #######
###########################################
#s: source word
#p: pivot word
#t: target word

pt_en_mr = {}
best_route_en_mr = {}

ditch = 0
for s in pt_en_hi:
    for p in pt_en_hi[s]:
        if not p in pt_hi_mr:
            ditch+=1
            continue
        if not s in pt_en_mr:
            pt_en_mr[s] = {}
        s_p_weight = pt_en_hi[s][p][2]
        p_s_weight = pt_en_hi[s][p][0]
        for t in pt_hi_mr[p]:
            if not t in pt_en_mr[s]:
                pt_en_mr[s][t] = [0.0, 0.0, 0.0, 0.0, 2.718, "A", "1 1 1"]
            multipliedprob = pt_en_hi[s][p][0]*pt_hi_mr[p][t][0]
            pt_en_mr[s][t][0]+= multipliedprob
            key = (s + "|||" + t)
            if not key in best_route_en_mr:
                best_route_en_mr[key] = [0, "ZZZ", "ZZZ"]
            if multipliedprob > best_route_en_mr[key][0]:
                best_route_en_mr[key][0] = multipliedprob 
                best_route_en_mr[key][1] = pt_en_hi[s][p][5]
                best_route_en_mr[key][2] = pt_hi_mr[p][t][5]

                
for s in pt_en_mr:
    for t in pt_en_mr[s]:
        key = (s + "|||" + t)
        a1 = best_route_en_mr[key][1]
        a2 = best_route_en_mr[key][2]
        combo = combinealignments(a1, a2)
        pt_en_mr[s][t][5] = combo


#Normalize:


#write pt_en_mr to file
out = open(file_en_mr, 'w')

for s in pt_en_mr:
    for t in pt_en_mr[s]:
        probs = " ".join([str(x) for x in pt_en_mr[s][t][0:5]])
        alignment = " ".join(pt_en_mr[s][t][5])
        counts = pt_en_mr[s][t][6]
        out.write(s + delim + t + delim + probs + delim + alignment + delim + counts + "\n")

out.close()

#        
#tocheck = pt_en_mr
#for a in tocheck:
#    sum = 0
#    for b in tocheck[a]:
#        sum+=tocheck[a][b][2]
#    if sum > 1.001 or sum<0.999: print a, sum
print "Done. Written to", file_en_mr