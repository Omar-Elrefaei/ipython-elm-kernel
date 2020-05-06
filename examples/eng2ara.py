import csv

arWords = []
enWords = []
with open('words.csv', newline='') as csvfile:
    words = csv.reader(csvfile, delimiter=',')
    for word in words:
        enWords.append(word[0])
        arWords.append(word[1])

with open('test.py', newline="\n") as codefile:
        for line in codefile:
            for (i,enWord) in enumerate(enWords):
                line = line.replace(enWord, arWords[i])
            print(line)
