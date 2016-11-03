#!/usr/bin/python
# -*- coding: utf8 -*-

#Liest Text aus einer Datei und versucht den Text zu entschlüsseln

import operator
import string
from collections import defaultdict

#Ermittlung der Häufigkeit eines Zeichens im Text
def getFrequencyOfACharInText(stringText,char):
    count = stringText.count(char)
    return count

#altes Wort wird mit einem neuerem Wort ersetzt und alle Buchstaben, die im Wort ersetzt werden müssen
#werden auch im gesamten Text geändert
def replaceWords(encryptedWord, newWord, decryptedText):
    i = 0
    for oldChar in encryptedWord:
        if oldChar != newWord[i]:
            decryptedText = decryptedText.replace(newWord[i], ".")
            tmp = oldChar
            decryptedText = decryptedText.replace(oldChar, newWord[i])
            decryptedText = decryptedText.replace(".", tmp)
        i += 1
    return decryptedText

def detectFrequencyofWordsWithGivenCountOfAChars(decryptedText, countOfChars):
    count = defaultdict(int)
    for c in decryptedText.split():
        if len(c) == countOfChars:
            count[c] += 1
    return count

#Liest verschlüsselten Text aus Datei
fobj = open("encryptedText.txt")
cryptedText = ""
for line in fobj:
    cryptedText += line.rstrip()
fobj.close()

#Erstellt Liste mit legalen Zeichen
legalChars = [chr(a + 97) for a in range(26)] + [" "]

# Entschlüsslungspart1
# Anzahl der der Häufigkeit der einzelnen Zeichen im legalem Zeichensatz ermitteln
i = 0
countLetter = legalChars[:]
for letter in legalChars:
    countLetter[i] = getFrequencyOfACharInText(cryptedText, letter)
    i += 1

#Beziegung zwischen Buchstabe und Häufigkeit setzen
legalCharsWithFrequency = dict(zip(legalChars, countLetter))

#Liste absteigend sortieren
sortedLegalCharsWithFrequency = sorted(legalCharsWithFrequency.items(), key=operator.itemgetter(1))
sortedLegalCharsWithFrequency.reverse()
print sortedLegalCharsWithFrequency

#absteigende Reihenfolge mit legale Zeichensatz(englisch)
listWithMostFrequencyLetterDesc = [" "]
countLetterEn = "etaoinshrdlcumwfgypbvkjxqz"
for item in countLetterEn:
    listWithMostFrequencyLetterDesc.append(item)

#nur die Buchstaben aus der Liste mit haeufigsten Zeichen im Text rausziehen
exctractedCharsFromList = []
for item in sortedLegalCharsWithFrequency:
    exctractedCharsFromList.append(item[0][0])

#Beziehung zwischen Häufigkeit im Text und Häufigkeit der Buchstaben im englsichen Sprachraum
#herstellen
codeBook = dict(zip(exctractedCharsFromList, listWithMostFrequencyLetterDesc))

#1. Versuch verschlüsselten Text zu entschlüssln
#Buchstabenersetzung
decryptedText = ""
for ch in cryptedText:
    decryptedText = decryptedText + codeBook[ch]

print decryptedText
splittedDecryptedText = string.split(decryptedText, " ")


#Ermittlung der Häufigkeit Wörter mit EINEM Zeichen
detectedWords= detectFrequencyofWordsWithGivenCountOfAChars(decryptedText, 1)
foundNewWord = sorted(detectedWords.items(), key=operator.itemgetter(1))

oneLetterWords = "ia"

i = 0
for oldChar in foundNewWord:
    oldChar = oldChar[0][0]
    if oldChar != oneLetterWords[i]:
            decryptedText = decryptedText.replace(oneLetterWords[i], ".")
            exctractedCharsFromList = oldChar
            decryptedText = decryptedText.replace(oldChar, oneLetterWords[i])
            decryptedText = decryptedText.replace(".", exctractedCharsFromList)
    i += 1
print decryptedText

#Häufigstes Wort mit 2 Buchstaben ermitteln und ersetzen
detectedWords = detectFrequencyofWordsWithGivenCountOfAChars(decryptedText, 2)
foundNewWord = sorted(detectedWords.items(), key=operator.itemgetter(1))
foundNewWord.reverse()
replaceWords(foundNewWord[0][0], "of", decryptedText)

#Häufigstes Wort mit 3 Buchstaben ermitteln und ersetzen
detectedWords = detectFrequencyofWordsWithGivenCountOfAChars(decryptedText, 3)
foundNewWord = sorted(detectedWords.items(), key=operator.itemgetter(1))
foundNewWord.reverse()
replaceWords(foundNewWord[0][0], "the", decryptedText)

"""#Häufigstes Wort mit 4 Buchstaben ermitteln und ersetzen
detectedWords = detectFrequencyofWordsWithGivenCountOfAChars(decryptedText, 4)
foundNewWord = sorted(detectedWords.items(), key=operator.itemgetter(1))
foundNewWord.reverse()
replaceWords(foundNewWord[0][0], "that", decryptedText)"""

"""#Häufigstes Wort mit 5 Buchstaben ermitteln
detectedWords = detectFrequencyofWordsWithGivenCountOfAChars(decryptedText, 5)
foundNewWord = sorted(detectedWords.items(), key=operator.itemgetter(1))
foundNewWord.reverse()
replaceWords(foundNewWord[0][0], "which", decryptedText)"""

splittedDecryptedText = string.split(decryptedText, " ")

stopper = 0
for token in splittedDecryptedText: #rekursion !!!!
#token = "alwags"
    print ">" + token
    lenToken = len(token)
    #print lenToken
    if lenToken >= 2 and lenToken <= 16:
        fobj = open("dict/" + str(lenToken) + "top.txt")
        foundWords = []
        maxCharsForAccord = (len(token)+1)/3*2
       # print maxCharsForAccord
        for line in fobj:
            dictWord = line.rstrip()
            if set(dictWord) == set(token):
                foundWords = []
                break
            if dictWord != token:
                i = 0
                count = 0
                for char in token:
                    if dictWord[i] == char:
                        count += 1
                    i += 1
                if count >= maxCharsForAccord:
                    foundWords.append(dictWord)
        print foundWords
        print len(foundWords)
        if len(foundWords) == 1:
            print foundWords
            decryptedText = replaceWords(token, foundWords[0], decryptedText)
        print decryptedText

        fobj.close()
    splittedDecryptedText = string.split(decryptedText, " ")
    print "stopper: " + str(stopper)
    stopper += 1
    if stopper == 52:
        break


print foundWords