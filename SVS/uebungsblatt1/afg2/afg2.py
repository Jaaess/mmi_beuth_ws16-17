# Aufgabe 2.1
# -*- coding: utf8 -*-

# Lösung von Steffen Burlefinger und Stephan Wagner

import math

costOneASIC = 50
costIntegrationOfOneASIC = 50
totalCostOfOneASIC = costOneASIC + costIntegrationOfOneASIC
budget = 1000000
totalASICSWithBudget = budget / totalCostOfOneASIC

print ""
print "Lösung 2.1.1:"
print "Wie viele Einheiten können mit dem zur Verfügung stehenden Etat parallel betrieben werden?"
print "Mit " + str(budget) + " Euro stehen " + str(totalASICSWithBudget) + " ASIC's parallel zur Verfügung!"


powerOneASIC = 5*(10**8)
powerOfAllASICS = totalASICSWithBudget * powerOneASIC
print ""
print "Lösung 2.1.2"
print "Wie lange dauert die durchschnittliche, die minimale und die maximale Schlüsselsuchzeit?"

ListWithKeyLengthinBits = [40, 56, 64, 112, 128]

def calculateKeyLength(bits):
    return 2**bits

def calculteKeySearchSime(bits):
    keyLen = calculateKeyLength(bits)
    minKeySearchTime = 1 / (powerOfAllASICS * keyLen)
    averageKeySearchTime = ((keyLen / 2) / powerOfAllASICS)
    maxKeySearchTime = keyLen / powerOfAllASICS

    print ""
    print "Suchzeiten mit " + str(bits) + " Bits in Sekunden"
    print "================================"
    print "Durchschnittliche Suchzeit mit Schlüssel: " + str(averageKeySearchTime)
    print "Minimale Suchzeit mit Schlüssel: " + str(minKeySearchTime)
    print "Maximal Suchzeit mit Schlüssel: " + str(maxKeySearchTime)

    print ""
    print "Suchzeiten mit " + str(bits) + " Bits in Minuten"
    print "================================"
    print "Durchschnittliche Suchzeit mit Schlüssel: " + str(averageKeySearchTime / 60)
    print "Minimale Suchzeit mit Schlüssel: " + str(minKeySearchTime / 60)
    print "Maximal Suchzeit mit Schlüssel: " + str(maxKeySearchTime / 60)

    print ""
    print "Suchzeiten mit " + str(bits) + " Bits in Stunden"
    print "================================"
    print "Durchschnittliche Suchzeit mit Schlüssel: " + str((averageKeySearchTime / 60) / 60)
    print "Minimale Suchzeit mit Schlüssel: " + str((minKeySearchTime / 60) / 60)
    print "Maximal Suchzeit mit Schlüssel: " + str((maxKeySearchTime / 60) / 60)

    return

for len in ListWithKeyLengthinBits:
    calculteKeySearchSime(len)

print "\n"
print "Lösung 2.2"
print "In wievielen Jahren könnte mit einem Etat von 1 Mrd Euro unter der Annahme "
print "der Weitergeltung von Moore’s Law eine Schlüsselsuchmaschine gebaut werden,"
print "welche eine durchschnittliche Suchzeit von 24 Stunden benötigt?"

print ""
print "Laut Moore's Law verdoppelt sich die Rechenleistung ca. alle 2 Jahre"
print ""

def mooresLaw(keyLen):
    budgetMooresLaw = 1000000000
    countOfAllASICSWithBudgetMooresLaw = budgetMooresLaw / costIntegrationOfOneASIC
    powerOfAllASICSWithBudgetMooresLaw = powerOneASIC * countOfAllASICSWithBudgetMooresLaw
    powerOfAllASICSWithBudgetMooresLawInHour = (powerOfAllASICSWithBudgetMooresLaw / 60) /60
    year = 2


    averageKey = (keyLen / 2)
    tmp = averageKey / (powerOfAllASICSWithBudgetMooresLawInHour / 24)
    result = math.log(tmp, 2) * year
    return round(result, 2)

for bit in ListWithKeyLengthinBits:
    keyLen = calculateKeyLength(bit)
    print "circa " + str(mooresLaw(keyLen)) + " Jahre benötigt man nach Moore's Law mit einer Schlüssellänge von " + str(keyLen)