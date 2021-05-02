# search datamuse for sound words beginning with letter
import requests, json, sys

letter = sys.argv[1]

apicall1 = "https://api.datamuse.com/words?ml=noise&sp=" + letter + "*&max=30"
apicall2 = "https://api.datamuse.com/words?ml=sound&sp=" + letter + "*&max=30"

r1 = requests.get(apicall1)
r2 = requests.get(apicall2)
j1 = json.loads(r1.text)
j2 = json.loads(r2.text)

words = []

for i in range(len(j1)):
    words.append(j1[i]['word'])
for i in range(len(j2)):
    words.append(j2[i]['word'])

for i in range(len(words)):
    print (words[i])