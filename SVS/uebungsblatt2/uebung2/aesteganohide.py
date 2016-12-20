#!/usr/bin/python
# -*- coding: utf8 -*-

import steganohide, sys, hashlib, hmac, os
from PIL import Image


def encryptMsg(mac, pw, txt):

    macSHA256 = hashlib.sha256(mac).digest()
    hashedMAC = hmac.new(macSHA256, txt, hashlib.sha256).digest()
    return hashedMAC + txt

def decryptMsg(mac, pw, imgFilename):

    macSHA256 = hashlib.sha256(mac).digest()

    getCryptedText = steganohide.readTxtFromImage(imgFilename)
    txt = getCryptedText[32:]

    hashedMAC = hmac.new(macSHA256, txt, hashlib.sha256).digest()
    potentialMAC = getCryptedText[0:32]

    if potentialMAC == hashedMAC:
        return txt
    else:
        return False

#Auf Anzahl der Parameter prüfen
if (not len(sys.argv) == 7) and (not len(sys.argv) == 8):
    sys.exit('Wrong count of parameters!\n'
             'example for encrypt: aesteganohide.py -e -m macpassword -k password text.txt bild.bmp\n'
             'example for decrypt: aesteganohide.py -d -m macpassword -k password bild.bmp')

mode = sys.argv[1]
if len(sys.argv) == 8 and mode == '-e':
    mac = sys.argv[3]
    pw = sys.argv[5]
    txtFilename = sys.argv[6]
    imgFilename = sys.argv[7]

    if steganohide.checkFileExistence(txtFilename, imgFilename):
        encryptedTxt = encryptMsg(mac, pw, steganohide.readTxtFile(txtFilename))
        if steganohide.writeTxtInImage(imgFilename, encryptedTxt):
            sys.exit('Successfull')
        else:
            sys.exit('Faild!')

elif len(sys.argv) == 7 and mode == '-d':
    mac = sys.argv[3]
    pw = sys.argv[5]
    imgFilename = sys.argv[6]

    if os.path.isfile(imgFilename):
        decryptedText = decryptMsg(mac, pw, imgFilename)
        if decryptedText != False:
            print decryptedText
        else:
            sys.exit('Wrong Password or corrupted File!')
else:
    sys.exit('Wrong mode! Operation failed!')
