import re

ptable=[]
suffix = "-100k"
path_ptable="../output/en-mr-phrase-table-phase1" + suffix
file_en_mr = "../output/en-mr-phrase-table-final" + suffix
delim = " ||| "

with open(path_ptable) as fp:
    for line in fp:
        row = line.split(delim)
        if not re.sub(" ", "", row[3]) == "":
            ptable.append(row)
        
# dictionary whose key are words and value is an index to another list
# which store count of that word with all the word of target language
src_word={}

# dictionary whose key are words and value is an index to another list
# which store count of that word with all the word of target language
trg_word={}

#------------------------------------------------end--------------------------------------------------------

# traverse the whole phrase table and store the words in dictionary(source in src_word and target in trg_word) and maintain its count
# This will help in speed up the code

count=-1


for line in ptable:
	words_src=line[0].split(' ')
	for word in words_src:
		if word in src_word:
			pass
		else:
			src_word[word]=count+1
			count+=1
count=-1		

for line in ptable:
	words_target=line[1].split(' ')
	for word in words_target:
		if word in trg_word:
			pass
		else:
			trg_word[word]=count+1
			count+=1	
	
src_trg_word_map=[]

for sourceword in src_word:	
	src_trg_word_map.append([])
for sourceword in src_word:	
	for targetword in trg_word:
		
		src_trg_word_map[src_word[sourceword]].append('0')


# Go to each phrase and update the cell of above list according to the formula(only those cell will be updated whoose word
# are present in that phrase). Here dictionary will help you to identify the cell(think how can you do that)

for line in ptable:
	alignmments=line[3].split(' ')
	for alignment in alignmments:
		sr,tr=alignment.split('-')
             
		
		srword=line[0].split(' ')[int(sr)]
		trword=line[1].split(' ')[int(tr)]

		src_trg_word_map[src_word[srword]][trg_word[trword]]=float(src_trg_word_map[src_word[srword]][trg_word[trword]])+float(line[2].split(' ')[0])


#print src_trg_word_map

word_prob_map=[]

for sourceword in src_word:
	word_prob_map.append([])

for sourceword in src_word:	
	for targetword in trg_word:
		word_prob_map[src_word[sourceword]].append('0')

for targetword in trg_word:
	sum=0
	for sourceword in src_word:
		sum=sum+float(src_trg_word_map[src_word[sourceword]][trg_word[targetword]])
	for sourceword in src_word:
		if sum>0:
			word_prob_map[src_word[sourceword]][trg_word[targetword]]=float(src_trg_word_map[src_word[sourceword]][trg_word[targetword]])/sum	

ctr=0
out = open(file_en_mr, 'w')
for line in ptable:
    ctr+=1
#    print ctr
    words_src=line[0].split(' ')
    product=1
    alignmments=line[3].split(' ')
    for i in range(len(words_src)):
        count=0
        sum=0
        for alignment in alignmments:
            sr,tr=alignment.split('-')
            srword=line[0].split(' ')[int(sr)]
            trword=line[1].split(' ')[int(tr)]
            if int(sr)==i:
                count+=1
                sum=sum+float(word_prob_map[src_word[srword]][trg_word[trword]])
            if count>0:
                product=product*sum/count    	
    values = line[2].split(' ')
    values[1] = product
    line[2] = " ".join([str(x) for x in values])
    #print line
    
    row = delim.join(line)
    out.write(row)
out.close()
    
    
