#!/usr/bin/python
# -*- coding: utf8 -*-

import steganohide
import sys
import hashlib
import hmac
import os
import binascii
import xtea
import string
import random

def encryptMsg(mac, pw, txt):

    macSHA256 = hashlib.sha256(mac).digest()
    hashedMAC = hmac.new(macSHA256, txt, hashlib.sha256).digest()
    hData = hashedMAC + txt

    hashedPW = hashlib.sha256(pw).digest()
    key = hashedPW[:16]
    IV = randomIV()
    x = xtea.new(key, mode=3, IV=IV)
    encryptedTxt =x.encrypt(hData)
    encryptedTxt = encryptedTxt.encode("hex")

    return IV.encode('hex') + encryptedTxt

def decryptMsg(mac, pw, imgFilename):
    macSHA256 = hashlib.sha256(mac).digest()
    hashedPW = hashlib.sha256(pw).digest()
    key = hashedPW[:16]

    getCryptedText = steganohide.readTxtFromImage(imgFilename)
    IV = getCryptedText[:16].decode('hex')
    x = xtea.new(key, mode=3, IV=IV)
    decryptedData = x.decrypt(getCryptedText[16:].decode('hex'))

    plaintxt = decryptedData[32:]

    hashedMAC = hmac.new(macSHA256, plaintxt, hashlib.sha256).digest()
    potentialMAC = decryptedData[0:32]

    if potentialMAC == hashedMAC:
        return plaintxt
    else:
        return False

def randomIV():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    result = ''
    for i in range(8):
        result += random.choice(chars)
    return result

#Auf Anzahl der Parameter prüfen
if (not len(sys.argv) == 7) and (not len(sys.argv) == 8):
    sys.exit('Wrong count of parameters!\n'
             'example for encrypt: aesteganohide.py -e -m macpassword -k password text.txt bild.bmp\n'
             'example for decrypt: aesteganohide.py -d -m macpassword -k password bild.bmp')

mode = sys.argv[1]
#Encoding-Modus
if len(sys.argv) == 8 and mode == '-e':

    mac = sys.argv[3]
    pw = sys.argv[5]
    txtFilename = sys.argv[6]
    imgFilename = sys.argv[7]

    if steganohide.checkFileExistence(txtFilename, imgFilename):
        encryptedTxt = encryptMsg(mac, pw, steganohide.readTxtFile(txtFilename))
        if steganohide.writeTxtInImage(imgFilename, encryptedTxt):
            sys.exit('Encoding Successfull')
        else:
            sys.exit('Encoding Faild!')
#Decoding-Modus
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