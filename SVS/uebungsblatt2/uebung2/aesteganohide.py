#!/usr/bin/python
# -*- coding: utf8 -*-

import steganohide
import sys
import hashlib
import hmac
import os
import math
import struct

def xteaAlgorithm(key,block,n=32,endian="!"):
    v0, v1 = struct.unpack(endian + "2L", block)
    k = struct.unpack(endian + "4L", key)
    sum, delta, mask = 0L, 0x9e3779b9L, 0xffffffffL
    for round in range(n):
        v0 = (v0 + (((v1 << 4 ^ v1 >> 5) + v1) ^ (sum + k[sum & 3]))) & mask
        sum = (sum + delta) & mask
        v1 = (v1 + (((v0 << 4 ^ v0 >> 5) + v0) ^ (sum + k[sum >> 11 & 3]))) & mask
    return struct.pack(endian + "2L", v0, v1)


def encryptCFB(key, data, iv='\00\00\00\00\00\00\00\00', n=32):
    block = iv
    result = ""
    for i in range(int(math.ceil(len(data) / 8.0))):
        plain = data[i * 8:i * 8 + 8]
        eKey  = xteaAlgorithm(key, block, n)

        xor = "".join([chr(ord(x)^ord(y)) for (x,y) in zip(plain, eKey)])
        result = result + xor
        block = xor

    return result

def decryptCFB(key, data, iv='\00\00\00\00\00\00\00\00', n=32):
    block = iv
    result = ""
    for i in range(int(math.ceil(len(data) / 8.0))):
        cipher = data[i * 8:i * 8 + 8]
        eKey = xteaAlgorithm(key, block, n)

        xor = "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(cipher, eKey)])
        result = result + xor
        block = cipher

    return result

def encryptMsg(mac, pw, txt):

    macSHA256 = hashlib.sha256(mac).digest()
    hashedMAC = hmac.new(macSHA256, txt, hashlib.sha256).digest()
    hData = hashedMAC + txt

    hashedPW = hashlib.sha256(pw).digest()
    key = hashedPW[:16]

    encryptedData = encryptCFB(key, hData)

    return encryptedData

def decryptMsg(mac, pw, imgFilename):
    macSHA256 = hashlib.sha256(mac).digest()
    hashedPW = hashlib.sha256(pw).digest()
    key = hashedPW[:16]

    getCryptedText = steganohide.readTxtFromImage(imgFilename)
    decryptedData = decryptCFB(key, getCryptedText)

    txt = decryptedData[32:]

    hashedMAC = hmac.new(macSHA256, txt, hashlib.sha256).digest()
    potentialMAC = decryptedData[0:32]

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
            sys.exit('Encoding Successfull')
        else:
            sys.exit('Encoding Faild!')

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
