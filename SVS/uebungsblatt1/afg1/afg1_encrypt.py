#!/usr/bin/python
# -*- coding: utf8 -*-

#Liest Text aus einer Datei und schreibt den verschüsselten Text in eine andere Datei

import random

def removeIllegalChars(realText,abc):
    newRealText = ""
    for rt in realText:
        for letter in abc:
            if letter == rt.lower():
                newRealText = newRealText + letter;
    return newRealText

#Legalen Zeichensatz erstellen
#legalChars = [chr(a+97) for a in range(26)] + [chr(b+65) for b in range(26)] + [' ']
abc = [chr(a+97) for a in range(26)] + [" "]

#legalen Zeichensatz kopieren und durcheinander wÃ¼rfeln
shuffled_abc = abc[:]
random.shuffle(shuffled_abc)

# Beziehung zwischen Zeichensatz und durchgewÃ¼rfelten Zeichensatz herstellen
wb = dict(zip(abc, shuffled_abc))

#Orginaltext aus Datei lesen
fobj = open("plainText2.txt")
getText = ""
for line in fobj:
    getText += line.rstrip()
fobj.close()

#Illegale Zeichen aus gelesenen Text entfernen
transformedRealText = removeIllegalChars(getText, abc)
print transformedRealText

#Text verschluesseln
cryptedText = ""
for c in transformedRealText:
    cryptedText = cryptedText+wb[c]
print cryptedText
#verschlüselten Text in Datei schreiben
fobj_out = open("encryptedText.txt","w")
fobj_out.write(cryptedText)
fobj_out.close()