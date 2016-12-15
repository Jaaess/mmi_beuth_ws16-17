#!/usr/bin/python
# -*- coding: utf8 -*-

import sys #Zum Abbrechen des Programms
import os.path #für die Prüfung der Existenz von Dateien
from PIL import Image
import binascii

PIXEL_BLOCK_LENGTH = 22
BIT_FIELD = 32

#Lesen der Textdatei
def readTxtFile(file):
    fobj = open(file)
    result = ""
    for line in fobj:
        result += line.rstrip().lower()
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

def intToBin(pixel):
    return bin(pixel)[2:].zfill(8)

def binToInt(bits):
    return int(bits, 2)

def lsb(bits, value):
    return bits[:-1]+value

def BinTxtLen(txt):
    txtLen = intToBin(len(txt))
    padding = '0'*(BIT_FIELD-len(txtLen))

    return padding + txtLen


#Schreibe Text in Bild
def writeTxtInImage(txt, image):
    img = Image.open(image)
    width, height = img.size

    txtToBin = bin(reduce(lambda x, y : (x<<8)+y, (ord(c) for c in txt), 1))[3:]
    print txtToBin

    txtToBinLen = BinTxtLen(txt)
    print txtToBinLen

    txtToBin = txtToBin + txtToBinLen
    print txtToBin

    txtIndex = 0
    if len(txtToBin) < width * height * 3:
        for h in range(height):
            for w in range(width):

                if txtIndex+3 <= len(txtToBin):

                    #Hole PixelInformationen
                    r, g, b = img.getpixel((w, h))

                    #Umwandlung von int-Value zu bin-Value
                    rBin = intToBin(r)
                    gBin = intToBin(g)
                    bBin = intToBin(b)


                    rLsb = lsb(rBin, txtToBin[txtIndex])
                    gLsb = lsb(gBin, txtToBin[txtIndex+1])
                    bLsb = lsb(bBin, txtToBin[txtIndex+2])

                    #Bits in Pixel schreiben
                    img.putpixel((w, h), (binToInt(rLsb), binToInt(gLsb), binToInt(bLsb)))

                elif(len(txtToBin) - txtIndex == 1):
                    rBin = intToBin(r)
                    rLsb = lsb(rBin, txtToBin[txtIndex])
                    img.putpixel((w, h), (binToInt(rLsb), g, b))

                elif(len(txtToBin) - txtIndex == 2):
                    rBin = intToBin(r)
                    rLsb = lsb(rBin, txtToBin[txtIndex])
                    gLsb = lsb(gLsb,txtToBin[txtIndex])
                    img.putpixel((w, h), (binToInt(rLsb), binToInt(gLsb), b))

                txtIndex += 3;

    else:
        sys.exit('Message to long')
        return False

    return True


def getBinTxtLen(img):
    width, height = img.size

    result = ''

    for h in range(height):

        for w in range(width):

            if h == 0 and w < PIXEL_BLOCK_LENGTH:
                r, g, b = img.getpixel((w, h))

                # Wandle RGB Werte (int) in (bin)
                rBit = intToBin(r)
                gBit = intToBin(g)
                bBit = intToBin(b)

                result += rBit[-1] + gBit[-1] + bBit[-1]

    return binToInt(result[:-2])


#Lesen des Textes aus einer Bild-Datei
def readTxtFromImage(image):
    img = Image.open(image)
    width, height = img.size

    txtLen = getBinTxtLen(img)
    print txtLen


    result = ''
    for h in range(height):
        for w in range(width):

            pixel = img.getpixel((w, h))

            # RGB Werte aus Pixel laden
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]

            # Wandle RGB Werte (int) in (bin)
            rBit = intToBin(r)
            gBit = intToBin(g)
            bBit = intToBin(b)

            result += rBit[-1] + gBit[-1] + bBit[-1]

            if len(result) >= (txtLen * 8) + BIT_FIELD:
                diff_end = (len(result) - BIT_FIELD) - (txtLen * 8)
                result = result[BIT_FIELD:]
                if diff_end == 0:
                    n = int(result, 2)
                    return binascii.unhexlify('%x' % n)

                else:
                    n = int(result[:-diff_end], 2)
                    return binascii.unhexlify('%x' % n)


#Auf Anzahl der Parameter prüfen
if len(sys.argv) != 3:
    sys.exit('Wrong count of parameters. We need two parameters - example: steganohide.py text.txt bild.bmp')

txtFilename = sys.argv[1]
imgFilename = sys.argv[2]

#Auf Existenz prüfen, falls erforgreich dann weiter
if checkFileExistence(txtFilename, imgFilename):
    if writeTxtInImage(readTxtFile(txtFilename), imgFilename):
        print 'Write text in image was successfull!'
        print readTxtFromImage(imgFilename)
    else:
        sys.exit('ERROR! Write text in image failed!')


# Let suppose an image has a size of 1200 * 800 pixel than 1200 x 800= 960,000 pixel
# so for 24-bit scheme that contain 3 bytes it would become 960,000 x 3 =28,80000 bytes and 1 byte consist of 8 bits so 2880000 x 8 = 23040000 bits

    #txtToInt = binascii.unhexlify('%x' % int(txtToBin, 2))
