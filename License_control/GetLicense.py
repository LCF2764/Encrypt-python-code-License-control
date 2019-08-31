# -*- coding: UTF-8 -*-
####################################
# TODO：从license.lic中解密出MAC地址
####################################
import os
import sys
import base64
import socket
import struct
import fcntl

from Crypto.Cipher import AES  
from binascii import b2a_hex, a2b_hex

seperateKey = "d#~0^38J:" 
aesKey = "123456789abcdefg" 
aesIv = "abcdefg123456789" 
aesMode = AES.MODE_CBC  # 使用CBC模式

def getHwAddr(ifname): 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
    return ''.join(['%02x' % ord(char) for char in info[18:24]])
    
def decrypt(text):
    try:
        cryptor = AES.new(aesKey, aesMode, aesIv)
    
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')
    except:
        return ""
    
def getLicenseInfo(filePath = None):
    if filePath == None:
        filePath = "./license.lic"
    
    if not os.path.isfile(filePath):
        return False, "Invalid"
    
    encryptText = "";
    with open(filePath, "r") as licFile:
        encryptText = licFile.read()
        licFile.close()
    try:
        hostInfo = getHwAddr('eth0')
    except IOError:
        hostInfo = getHwAddr('eno1')
    
    decryptText = decrypt(encryptText)
    pos = decryptText.find(seperateKey)
    if -1 == pos:
        return False, "Invalid"
    licHostInfo = decrypt(decryptText[0:pos])
    licenseStr = decryptText[pos + len(seperateKey):]
    # print licHostInfo, licenseStr
    
    if licHostInfo == hostInfo:
        return True, licenseStr
    else:
        return False, "Invalid"

if __name__ == "__main__":
    status, licInfo = getLicenseInfo()
    print status, licInfo
