# coding:utf-8
import socket, fcntl, datetime, os, struct
from Crypto.Cipher import AES 
from binascii import b2a_hex, a2b_hex 

class Get_License(object):
    def __init__(self):
        super(Get_License, self).__init__()
        
        # 定义秘钥信息
        self.seperateKey = "d#~0^38J:"
        self.aesKey = "123456789abcdefg"
        self.aesIv = "abcdefg123456789"
        self.aesMode = AES.MODE_CBC

    def getHwAddr(self, ifname):
        """
        获取主机物理地址
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
        return ''.join(['%02x' % ord(char) for char in info[18:24]])
        
    def decrypt(self, text):
        """
        从.lic中解密出主机地址
        """
        try:
            cryptor = AES.new(self.aesKey, self.aesMode, self.aesIv)
        
            plain_text = cryptor.decrypt(a2b_hex(text))
            return plain_text.rstrip('\0')
        except:
            return ""
        
    def getLicenseInfo(self, filePath = None):
        if filePath == None:
            filePath = "./license.lic"
        
        if not os.path.isfile(filePath):
            print("请将 license.lic 文件放在当前路径下")
            os._exit(0)
            return False, 'Invalid'             
        
        encryptText = ""
        with open(filePath, "r") as licFile:
            encryptText = licFile.read()
            licFile.close()
        try:
            hostInfo = self.getHwAddr('eth0')
        except IOError:
            hostInfo = self.getHwAddr('eno1')
        
        decryptText = self.decrypt(encryptText)
        pos = decryptText.find(self.seperateKey)
        if -1 == pos:
            return False, "Invalid"
        licHostInfo = self.decrypt(decryptText[0:pos])
        licenseStr = decryptText[pos + len(self.seperateKey):]

        if licHostInfo == hostInfo:
            return True, licenseStr
        else:
            return False, 'Invalid'

License = Get_License()
condition, LicInfo = License.getLicenseInfo()


class Today():
    def get_time(self):
        if condition==True and LicInfo=='Valid':
            print(datetime.datetime.now())
        else:
            print('未权授！')

    def say(self):
        if condition==True and LicInfo=='Valid':
            print('hello world!')
        else:
            print('未权授！')

