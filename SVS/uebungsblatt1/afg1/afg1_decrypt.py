#!/usr/bin/python
# -*- coding: utf8 -*-

#Liest Text aus einer Datei und versucht den Text zu entschlüsseln

import operator
import string
import enchant #externe Bibliothek

import re
from collections import Counter
from collections import defaultdict
def getFrequencyOfACharInText(stringText,char):
    count = stringText.count(char)
    #return "Char: %c = %i " % (char, count)
    return count

fobj = open("encryptedText.txt")
cryptedText = ""
for line in fobj:
    cryptedText += line.rstrip()
fobj.close()

abc = [chr(a+97) for a in range(26)] + [" "]

# Entschlüsslungspart
# Anzahl der der Häufigkeit der einzelnen Zeichen im legalem Zeichensatz ermitteln
i = 0
countLetter = abc[:]
for letter in abc:
    countLetter[i] = getFrequencyOfACharInText(cryptedText, letter)
    i += 1
#Beziegung zwischen Buchstabe und Häufigkeit setzen
countAbc = dict(zip(abc, countLetter))

#Liste absteigend sortieren
sortedCountAbc = sorted(countAbc.items(), key=operator.itemgetter(1))
sortedCountAbc.reverse()
print sortedCountAbc

#absteigende Reihenfolge mit legale Zeichensatz(englisch)
aCountLetterEn = [" "]
countLetterEn = "etaoinshrdlcumwfgypbvkjxqz"
#countLetterEn = "et"
for item in countLetterEn:
    aCountLetterEn.append(item)
#print aCountLetterEn

#nur die Buchstaben aus der Liste mit haeufigsten Zeichen im Text rausziehen
tmp = []
for item in sortedCountAbc:
    tmp.append(item[0][0])

#Beziehung zwischen Häufigkeit im Text und Häufigkeit der Buchstaben im englsichen Sprachraum
#herstellen
cb = dict(zip(tmp, aCountLetterEn))

#1. Versuch verschlüsselten Text zu entschlüssln
#Buchstabenersetzung
decryptedText = ""
for ch in cryptedText:
    decryptedText = decryptedText+cb[ch]

print decryptedText

splittedDecryptedText = string.split(decryptedText, " ")
#print splittedDecryptedText

#Häufigstes Wort mit 3 Buchstaben ermitteln
d = defaultdict(int)
for w in decryptedText.split():
    if len(w) >= 3:
        d[w] += 1

sortedFrequencyThreeLetterWords = sorted(d.items(), key=operator.itemgetter(1))
sortedFrequencyThreeLetterWords.reverse()
print sortedFrequencyThreeLetterWords[0][0]

mostFrequencyWordWithThreeLetter = "the"

#Das häufigste Wort mit 3 Buchstaben mit "the" ersetzen
i = 0
for oldChar in sortedFrequencyThreeLetterWords[0][0]:
    if oldChar != mostFrequencyWordWithThreeLetter[i]:
            decryptedText = decryptedText.replace(mostFrequencyWordWithThreeLetter[i], ".")
            tmp = oldChar
            decryptedText = decryptedText.replace(oldChar, mostFrequencyWordWithThreeLetter[i])
            decryptedText = decryptedText.replace(".", tmp)
    i += 1
print decryptedText


#Häufigstes Wort mit 2 Buchstaben ermitteln
d = defaultdict(int)
for w in decryptedText.split():
    if len(w) >= 2:
        d[w] += 1

sortedFrequencyThreeLetterWords = sorted(d.items(), key=operator.itemgetter(1))
print sortedFrequencyThreeLetterWords.reverse()
#print sortedFrequencyThreeLetterWords[0][0]

mostFrequencyWordWithThreeLetter = "the"

"""j = 0
for token in splittedDecryptedText:
#for x in range(0, 10):
    #token = splittedDecryptedText[x]
    print "token: " + token
    en = enchant.Dict("en_EN")
    us = enchant.Dict("en_US")
    results_en = en.suggest(token)
    results_us = us.suggest(token)
    print results_en
    print results_us

    hit = False
    hitWord = ""
    for item in results_en:
        for item2 in results_us:
            if len(item) == len(token) == len(item2):
                if item.lower() == item2.lower():
                    hitWord = item.lower()
                    hit = True
                    break
        if hit:
            break

    print hitWord
    print hit
    if hit and len(hitWord) > 0:
        print hit

        i = 0
        for newChar in hitWord:
            oldChar = splittedDecryptedText[j][i]
            decryptedText = decryptedText.replace(newChar, ".")
            tmp = oldChar
            decryptedText = decryptedText.replace(oldChar, newChar)
            decryptedText = decryptedText.replace(".", tmp)
            i += 1
    j += 1
    #print j
    print decryptedText
    splittedDecryptedText = string.split(decryptedText, " ")
    print splittedDecryptedText"""

#http://www.mathe.tu-freiberg.de/~hebisch/cafe/kryptographie/bigramme.html
#http://www.mathe.tu-freiberg.de/~hebisch/cafe/kryptographie/haeufigkeitstabellen.html