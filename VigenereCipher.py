import operator
from itertools import islice

cipherText = "RLWRVMRLAQEDUEQQWGKILFMFEXZYXAQXGJHFMXKMQWRLALKLFELGWCLSOLMXRLWPIOCVWLSKNISIMFESJUVARMFEXZCVWUSMJHTCRGRVMRLSZSMREFWXZGRYRLWPIOMYDBSFJCTCAZYXAQ"
codeFrequency = {"G1": {}, "G2": {}, "G3": {}}  # dict{grp {letters: freq}}
codeFrequency1 = {"G1": {}, "G2": {}, "G3": {}}
englishFreaquency = {"A": 8.16, "B": 1.49, "C": 2.78, "D": 4.25, "E": 12.7, "F": 2.22, "G": 2.01, "H": 6.09, "I": 6.96,
                     "J": 0.15, "K": 0.77, "L": 4.02, "M": 2.4, "N": 6.74, "O": 7.5, "P": 1.92, "Q": 0.09, "R": 5.98,
                     "S": 6.32, "T": 9.05, "U": 2.75, "V": 0.97, "W": 2.36, "X": 0.15, "Y": 1.97, "Z": 0.07}
groups = {"G1": [], "G2": [], "G3": []}  # dict{grpID : [letters of grp]}

keysG1 = []
keysG2 = []
keysG3 = []

def splitMsg(cipherText):
    for i in range(0, len(cipherText)):
        if i % 3 == 0:
            # print(cipherText[i])
            groups["G1"].append(cipherText[i])
        elif i % 3 == 1:
            groups["G2"].append(cipherText[i])
        elif i % 3 == 2:
            groups["G3"].append(cipherText[i])
    print(groups.get("G1"))
    print(groups.get("G2"))
    print(groups.get("G3"))


splitMsg(cipherText)


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


def frequencyCompute(G):
    for s in groups.get(G):
        if s in codeFrequency.get(G):
            codeFrequency.get(G)[s] += 1
        else:
            codeFrequency.get(G)[s] = 1
#    for s in codeFrequency.get(G):
#        codeFrequency.get(G)[s]= codeFrequency.get(G).get(s)/len(groups.get(G))

frequencyCompute("G1")
frequencyCompute("G2")
frequencyCompute("G3")
print("HEEEEEEEEEEEEEERE")
print(codeFrequency)
# sorted freqency map
sortedMap = {"G1": sorted(codeFrequency.get("G1").items(), key=operator.itemgetter(1), reverse=True),
             "G2": sorted(codeFrequency.get("G2").items(), key=operator.itemgetter(1), reverse=True),
             "G3": sorted(codeFrequency.get("G3").items(), key=operator.itemgetter(1), reverse=True)}
sortedEngMap = sorted(englishFreaquency.items(), key=operator.itemgetter(1), reverse=True)
print("SORTED MAP")
print(sortedMap)
print("SORTED ENGLISH MAP")
print(sortedEngMap)

# dict{G:[string keys]} = G1[0]-Eng[mos frequence]
# dict{grp : {letters: freq}}
commonLetters = {"G1": take(3, sortedMap.get("G1")), "G2": take(3, sortedMap.get("G2")),
                 "G3": take(3, sortedMap.get("G3")), "ENG": take(3, sortedEngMap)}
potentialKeys = {"G1": [x[0] for x in commonLetters.get("G1")], "G2": [x[0] for x in commonLetters.get("G2")],
                 "G3": [x[0] for x in commonLetters.get("G3")], "ENG": [x[0] for x in commonLetters.get("ENG")]}
print(potentialKeys)

def decrypt():
    for i in range(3):
       keysG1.append(chr((ord(potentialKeys.get("G1")[0]) - ord(potentialKeys.get("ENG")[i]))%26 + 65))
       keysG2.append(chr((ord(potentialKeys.get("G2")[0]) - ord(potentialKeys.get("ENG")[i]))%26 + 65))
       keysG3.append(chr((ord(potentialKeys.get("G3")[0]) - ord(potentialKeys.get("ENG")[i]))%26 + 65))
    print(keysG1)
    print(keysG2)
    print(keysG3)

decrypt()
