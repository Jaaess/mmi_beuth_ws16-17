#!/usr/bin/python
# -*- coding: utf8 -*-

import sys #Zum Abbrechen des Programms
import os.path #für die Prüfung der Existenz von Dateien
from PIL import Image
import binascii

#Lesen der Textdatei
def readTxtFile(file):
    fobj = open(file)
    result = ""
    for line in fobj:
        result += line.rstrip()#.lower()
    fobj.close()

    return result

#Prüft, ob Textdatei und Bild existieren
def checkFileExistence(txt, img):
    txtExist = False
    imgExist = False
    if os.path.isfile(txt):
        txtExist = True
    else:
        sys.exit(txt + ' not exist!')

    if os.path.isfile(img):
        imgExist = True
    else:
        sys.exit(img + ' not exist')

    if txtExist and imgExist:
        return True
    else:
        return False

def rgbCodeToHexcode(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hexcodeTorgbCode(hexcode):
    return tuple(map(ord, hexcode[1:].decode('hex')))

def stringToBinary(message):
    binary = bin(int(binascii.hexlify(message), 16))
    return binary[2:]

def binaryToString(binary):
    message = binascii.unhexlify('%x' % (int('0b' + binary, 2)))
    return message

def encode(hexcode, digit):
    if hexcode[-1] in ('0', '1', '2', '3', '4', '5'):
        hexcode = hexcode[:-1] + digit
        return hexcode
    else:
        return None

def decode(hexcode):
    if hexcode[-1] in ('0', '1'):
        return hexcode[-1]
    else:
        return None

#Schreiben in Bild-Datei
def writeTxtInImage(imgFilename, message):
    img = Image.open(imgFilename)
    binary = stringToBinary(message) + '1111111111111110'
    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()

        newData = []
        digit = 0
        for item in datas:
            if (digit < len(binary)):
                newpix = encode(rgbCodeToHexcode(item[0], item[1], item[2]), binary[digit])
                if newpix == None:
                    newData.append(item)
                else:
                    r, g, b = hexcodeTorgbCode(newpix)
                    newData.append((r, g, b, 255))
                    digit += 1
            else:
                newData.append(item)

        img.putdata(newData)
        img.save(imgFilename + ".sae", "PNG")
        return True

    return False


#Lesen aus Bild-Datei
def readTxtFromImage(filename):
    img = Image.open(filename + ".sae")
    binary = ''

    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()

        for item in datas:
            digit = decode(rgbCodeToHexcode(item[0], item[1], item[2]))
            if digit == None:
                pass
            else:
                binary = binary + digit
                if (binary[-16:] == '1111111111111110'):
                    return binaryToString(binary[:-16])

        return binaryToString(binary)
    return False
