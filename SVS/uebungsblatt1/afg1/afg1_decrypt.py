#!/usr/bin/python
# -*- coding: utf8 -*-

# Lösung von Steffen Burlefinger und Stephan Wagner

#Liest Text aus einer Datei und versucht den Text zu entschlüsseln

import operator
import string
from collections import defaultdict
import enchant


#Ermittlung der Häufigkeit eines Zeichens im Text
def getFrequencyOfACharInText(stringText,char):
    count = stringText.count(char)
    return count

#altes Wort wird mit einem neuerem Wort ersetzt und alle Buchstaben, die im Wort ersetzt werden müssen
#werden auch im gesamten Text geändert
def replaceWords(encryptedWord, newWord, decryptedText):
    i = 0
    #switchedChar = []
    for oldChar in encryptedWord:
        if oldChar != newWord[i]:
            decryptedText = decryptedText.replace(newWord[i], ".")
            tmp = oldChar
            decryptedText = decryptedText.replace(oldChar, newWord[i])
            decryptedText = decryptedText.replace(".", tmp)
        i += 1
    return decryptedText

#Analysiert wieviel Wörter es mit einer bestimmten Anzahl von Buchstaben existieren
#und gibt das Ergebnis zurück
def detectFrequencyofWordsWithGivenCountOfAChars(decryptedText, countOfChars):
    count = defaultdict(int)
    for c in decryptedText.split():
        if len(c) == countOfChars:
            count[c] += 1
    return count


# Wörter eine Liste schreiben die noch unbekannte Buchstaben besitzen
def getWordsWithUnknownLetter(text, listWithWithKnownLetters):
    splittedDecryptedText = string.split(decryptedText, " ");
    wordsWithUnknownLetters = [];
    for token in splittedDecryptedText:
        for char in token:
            if char not in foundChars:
                wordsWithUnknownLetters.append(token)
    wordsWithUnknownLetters = sorted(list(set(wordsWithUnknownLetters)))
    return wordsWithUnknownLetters

#Liest verschlüsselten Text aus Datei
fobj = open("encryptedText.txt")
cryptedText = ""
for line in fobj:
    cryptedText += line.rstrip()
fobj.close()
print "Ausgabe des verschüsselten Textes:"
print cryptedText

#Erstellt Liste mit legalen Zeichen
legalChars = [chr(a + 97) for a in range(26)] + [" "]

# Entschlüsslungspart1
# Anzahl der der Häufigkeit der einzelnen Zeichen im legalem Zeichensatz ermitteln
i = 0
countLetter = legalChars[:]
for letter in legalChars:
    countLetter[i] = getFrequencyOfACharInText(cryptedText, letter)
    i += 1

#Beziehung zwischen Buchstabe und Häufigkeit setzen
legalCharsWithFrequency = dict(zip(legalChars, countLetter))

#Liste absteigend sortieren
sortedLegalCharsWithFrequency = sorted(legalCharsWithFrequency.items(), key=operator.itemgetter(1))
sortedLegalCharsWithFrequency.reverse()
print "\nHäufgikeit der Buchstaben im verschlüsselten Text:"
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

#Beziehung zwischen Häufigkeit im Text und Häufigkeit der Buchstaben im englsichen Sprachraum herstellen
codeBook = dict(zip(exctractedCharsFromList, listWithMostFrequencyLetterDesc))

#1. Versuch verschlüsselten Text zu entschlüssln
#Buchstabenersetzung
decryptedText = ""
for ch in cryptedText:
    decryptedText = decryptedText + codeBook[ch]

splittedDecryptedText = string.split(decryptedText, " ")
print "\nAusgabe nach Analyse und Austausch der Buchstaben:"
print decryptedText

#Ermittlung der Häufigkeit Wörter mit EINEM Zeichen
detectedWords = detectFrequencyofWordsWithGivenCountOfAChars(decryptedText, 1)
foundNewWord = sorted(detectedWords.items(), key=operator.itemgetter(1))
if len(foundNewWord) == 2:
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
print "\nAusgabe nach ein- und ersetzen von Wörtern mit der Buchstabenlänge von eins:"
print decryptedText

#Häufigstes Wort mit 2 Buchstaben ermitteln und ersetzen
detectedWords = detectFrequencyofWordsWithGivenCountOfAChars(decryptedText, 2)
foundNewWord = sorted(detectedWords.items(), key=operator.itemgetter(1))
foundNewWord.reverse()
decryptedText = replaceWords(foundNewWord[0][0], "of", decryptedText)
print "\nAusgabe nach ein- und ersetzen von Wörtern mit der Buchstabenlänge von zwei:"
print decryptedText

#Häufigstes Wort mit 3 Buchstaben ermitteln und ersetzen
detectedWords = detectFrequencyofWordsWithGivenCountOfAChars(decryptedText, 3)
foundNewWord = sorted(detectedWords.items(), key=operator.itemgetter(1))
foundNewWord.reverse()
decryptedText = replaceWords(foundNewWord[0][0], "the", decryptedText)
print "\nAusgabe nach ein- und ersetzen von Wörtern mit der Buchstabenlänge von drei:"
print decryptedText

#Häufigstes Wort mit 4 Buchstaben ermitteln und ersetzen
detectedWords = detectFrequencyofWordsWithGivenCountOfAChars(decryptedText, 4)
foundNewWord = sorted(detectedWords.items(), key=operator.itemgetter(1))
foundNewWord.reverse()
replaceWords(foundNewWord[0][0], "that", decryptedText)
print "\nAusgabe nach ein- und ersetzen von Wörtern mit der Buchstabenlänge von vier:"
print decryptedText

splittedDecryptedText = string.split(decryptedText, " ")
foundChars = [' ', 'e', 't', 'h', 'w', 'a', 'o', 'f', 'i']


#Lokales Wörterbuchcheck
print "\nAusgabe nach Wörterbuch-Check:"
stopper = 0
for x in range(0, len(splittedDecryptedText)):
    token = splittedDecryptedText[x]
    lenToken = len(token)
    if lenToken >= 2 and lenToken <= 16:
        fobj = open("dict/" + str(lenToken) + "top.txt")
        foundWords = []
        maxCharsForAccord = (len(token)+1)/3*2
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
        tmp = []
        for word in foundWords:
            for letter in word:
                matching = letter not in foundChars
                if matching:
                    tmp.append(word)
                    break
        foundWords = tmp
        if len(foundWords) == 1:
            decryptedText = replaceWords(token, foundWords[0], decryptedText)
            for letter in foundWords[0]:
                foundChars.append(letter)
            foundChars = list(set(foundChars))
        fobj.close()
    splittedDecryptedText = string.split(decryptedText, " ")
    stopper += 1
    if stopper == 50:
        break

print decryptedText


print "\nAusgabe nach PyEnchant-Check: "
wordsWithUnknownLetter = getWordsWithUnknownLetter(decryptedText, foundChars)
enchantUS = enchant.Dict("en_US")

#Alle Wörter rausschmeissen von den alle befindlichen Buchstaben bekannt sind
removeWords = []
for token in wordsWithUnknownLetter:
    enchantResult = enchantUS.suggest(token)
    for result in enchantResult:
        if str.lower(result) == token:
            for letter in token:
                if letter not in foundChars:
                    foundChars.append(letter)
            removeWords.append(token)
            continue
for word in removeWords:
    if word in wordsWithUnknownLetter:
        wordsWithUnknownLetter.remove(word)

wordsWithUnknownLetter = getWordsWithUnknownLetter(decryptedText, foundChars)
finished = False

#mit PyEnchant die letzten Wörter rausfinden und mit dem Text abgleichen
if len(wordsWithUnknownLetter) > 0:
    while finished == False:
        enchantResult = enchantUS.suggest(wordsWithUnknownLetter[0])
        before = wordsWithUnknownLetter[0];
        tmpRemove = []
        for result in enchantResult:
            if len(wordsWithUnknownLetter) > 0:
                if len(result) == len(wordsWithUnknownLetter[0]):
                    for letter in str.lower(result):
                        if letter not in foundChars:
                            foundChars.append(letter)
                            index = decryptedText.find(letter)
                            tmpDecryptedText = replaceWords(wordsWithUnknownLetter[0], result, decryptedText)
                            decryptedText[index]
                            if tmpDecryptedText[index] not in foundChars:
                                foundChars.append(decryptedText[index])
                                decryptedText = tmpDecryptedText
                                wordsWithUnknownLetter = getWordsWithUnknownLetter(decryptedText, foundChars)
                            if len(wordsWithUnknownLetter) == 0:
                                finished = True
        if len(wordsWithUnknownLetter) > 0:
            if before == wordsWithUnknownLetter[0]:
                tmpRemove.append(wordsWithUnknownLetter[0])
                wordsWithUnknownLetter.remove(wordsWithUnknownLetter[0])
                if len(wordsWithUnknownLetter) == 0:
                    finished = True

print decryptedText

fobj = open("plainText2.txt")
plainText = ""
for line in fobj:
    plainText += line.rstrip()
fobj.close()

print "\nORIGINAL-TEXT:"
print plainText