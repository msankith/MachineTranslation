

phraseTable="/home/ankith/learning/nlp/pivotbased/en-mr-direct/phrase-table_original-despaced"
phraseTable2="../en-mr-phrase-table-final-100k"
outputF="../phrase-table-append"
f=open(phraseTable,'r')
w=open(outputF,'w')
delim=" ||| "
pt_en_hi={}
for line in f:
	row=line.split(delim)
	en=row[0]
	#prob_numbers=row[2]
	#probs=[float(x) for x in (prob_numbers.split(' '))]
	if not en in pt_en_hi:
		pt_en_hi[en]={}
		

f.close()
f=open(phraseTable2,'r')
for line in f:
	row=line.split(delim)
	en=row[0]
	if not en in pt_en_hi:
		w.write(line)
w.close()	

