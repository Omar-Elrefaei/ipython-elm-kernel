import csv
import re

arWords = []
enWords = []
with open('enSorted.csv', newline='') as csvfile:
    words = csv.reader(csvfile, delimiter=',')
    for word in words:  # 0,1 = en > ar
        enWords.append(word[1])
        arWords.append(word[0])

qoute_regex_original = r'(\'.*?(?<!\\)\')|(".*?(?<!\\)")'
qoute_regex = re.compile(qoute_regex_original)

delms = ["(", ")", " ", ":", "\"", "'", "=", "+", "-", "!", "&",
         "^", "*", "[", "]", ";", ".", ",", "/", "<", ">"]
temp_str = "(" + '|'.join(map(re.escape, delms)) + ")"
delms_regex = re.compile(temp_str)


def transpile(lines):
    # Concate lines ending with "\" to split on qoutes properly
    multiline_code = ""
    for line in lines:
        multiline_code += line
    no_multiline_code = re.sub(r'\\\n', '', multiline_code)
    no_multiline_code = no_multiline_code.split("\n")

    transpiled_code = []
    for line in no_multiline_code:
        # Separate code and string literals
        phrases = re.split(qoute_regex, line)
        for i in range(phrases.count(None)):
            phrases.remove(None)
        for i in range(phrases.count("")):
            phrases.remove("")

        for j, phrase in enumerate(phrases):
            if (phrase[0] == "'") | (phrase[0] == '"'):
                continue
            else:
                # for every code phrase, split words and try to translate them
                words = re.split(delms_regex, phrase)
                for x in range(len(words)):
                    for i in range(len(enWords)):
                        if words[x] == enWords[i]:
                            words[x] = arWords[i]
                phrase = ''.join(words)
                phrases[j] = phrase
        line = ''.join(phrases)
        transpiled_code.append(line + "\n")
    return(transpiled_code)


# For testing. [TODO: delete?]
if __name__ == "__main__":
    with open('qoute-test.py', newline="\n") as codefile:
        fixed_code = transpile(codefile)
        for line in fixed_code:
            print(line, end="")
