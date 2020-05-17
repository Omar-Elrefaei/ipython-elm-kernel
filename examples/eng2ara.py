import csv
import re
arWords = []
enWords = []
with open('enSorted.csv', newline='') as csvfile:
	words = csv.reader(csvfile, delimiter=',')
	for word in words:
		enWords.append(word[0])
		arWords.append(word[1])



delms = ["(",")"," ",":","\"","'","=","+","-","!","&","^","*","[","]",";",".",",","/","<",">"]
temp_str = "("+'|'.join(map(re.escape, delms))+")"
delms_regex = re.compile(temp_str)

with open('test.py', newline="\n") as codefile:
	for line in codefile:
		words = delms_regex.split(line)
		for x in range(len(words)):
			for i in range(len(enWords)):
				if words[x] == enWords[i]: 
					words[x] = arWords[i]
		line = ''.join(words)
		print(line, end="")