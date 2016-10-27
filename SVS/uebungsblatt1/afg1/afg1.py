#!/usr/bin/python
# -*- coding: latin-1 -*-

import random
import operator

def removeIllegalChars(realText,abc):
    newRealText = ""
    for rt in realText:
        for letter in abc:
            if letter == rt.lower():
                newRealText = newRealText + letter;
    return newRealText

def getFrequencyOfACharInText(stringText,char):
    count = stringText.count(char)
    #return "Char: %c = %i " % (char, count)
    return count

#Legalen Zeichensatz erstellen
#abc = [chr(a+97) for a in range(26)] + [chr(b+65) for b in range(26)] + [' ']
abc = [chr(a+97) for a in range(26)] + [" "]

#legalen Zeichensatz kopieren und durcheinander würfeln
shuffled_abc = abc[:]
random.shuffle(shuffled_abc)

# Beziehung zwischen Zeichensatz und durchgewürfelten Zeichensatz herstellen
wb = dict(zip(abc, shuffled_abc))

#Orginaltext aus Datei lesen
fobj = open('text.txt')
getText = ""
for line in fobj:
    getText += line.rstrip()
fobj.close()

#Illegale Zeichen aus gelesenen Text entfernen
transformedRealText = removeIllegalChars(getText, abc)
print transformedRealText
print

#Text verschlüsseln
cryptedText = ""
for c in transformedRealText:
    cryptedText = cryptedText+wb[c]
print cryptedText
print

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
print

#absteigende Reihenfolge mit legale Zeichensatz(englisch)
aCountLetterEn = [" "]
countLetterEn = "etaoinshrdlcumwfgypbvkjxqz"
for item in countLetterEn:
    aCountLetterEn.append(item)

#nur die Buchstaben aus der Liste mit häufgsten Zeichen im Text rausziehen
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

print transformedRealText
print
print decryptedText
print



#http://www.mathe.tu-freiberg.de/~hebisch/cafe/kryptographie/bigramme.html
#http://www.mathe.tu-freiberg.de/~hebisch/cafe/kryptographie/haeufigkeitstabellen.html
