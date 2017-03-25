

phraseTable="../en-mr-phrase-table-final-100k"
outputF="../phrase-table-prune"
f=open(phraseTable,'r')
w=open(outputF,'w')
delim=" ||| "
threshold=0.4
for line in f:
	row=line.split(delim)
	prob_numbers=row[2]
	probs=[float(x) for x in (prob_numbers.split(' '))]
	if (probs[0] >threshold):
		#print line
		w.write(line)
w.close()	

