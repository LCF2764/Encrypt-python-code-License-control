# -*- coding: UTF-8 -*-
# 获取计算机的物理地址

import socket
import struct
import fcntl

def getHwAddr(ifname): 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
    return ''.join(['%02x' % ord(char) for char in info[18:24]])
    

if __name__ == '__main__':
	try:
		print(getHwAddr('eth0'))
	except IOError:
		print(getHwAddr('eno1'))

