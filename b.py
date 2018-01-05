#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import struct

def save_file(file_name, data):  
    file=open(file_name, "wb")  
    file.write(data)   
    file.flush()  
    file.close()


TIMEOUT = 15
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(TIMEOUT)

s.connect(('127.0.0.1', 1313))

readBannerBytes = 0
bannerLength = 2
readFrameBytes = 0
frameBodylength = 0
dataBody = ""

version = 0
pid = 0
RealWidth = 0
RealHeight = 0
VirtualWidth = 0
VirtualHeight = 0
Orientation =0
Quirks = 0



while True:
    chunk = s.recv(4096)
    length = len(chunk)
    print 'length = ' + str(length)
    # if not length:
    #     continue      
    cursor = 0
    while cursor < length:
        #just do it            
        if readBannerBytes < bannerLength:
            print 'readBannerBytes = '+ str(readBannerBytes)
            if readBannerBytes==0:
                version = int(chunk[cursor].encode('hex'), 16)
                print 'version = ' +str(version)
            elif readBannerBytes==1:
                bannerLength = int(chunk[cursor].encode('hex'), 16)
                print 'bannerLength = ' + str(bannerLength)
            elif readBannerBytes in [2,3,4,5]:
                # self.banner.Pid += (bytes_to_int(chunk[cursor]) << ((readBannerBytes - 2) * 8)) >> 0;
                pid += (int(chunk[cursor].encode('hex'), 16) << ((readBannerBytes - 2) * 8)) >> 0
                print 'pid = ' + str(pid)
            elif readBannerBytes in [6,7,8,9]:
                RealWidth += (int(chunk[cursor].encode('hex'), 16) << ((readBannerBytes - 6) * 8)) >> 0
                print 'RealWidth = ' + str(RealWidth)
            elif readBannerBytes in [10,11,12,13]:
                RealHeight += (int(chunk[cursor].encode('hex'), 16) << ((readBannerBytes - 10) * 8)) >> 0
                print 'RealHeight = ' + str(RealHeight)
            elif readBannerBytes in [14,15,16,17]:
                VirtualWidth += (int(chunk[cursor].encode('hex'), 16) << ((readBannerBytes - 14) * 8)) >> 0
                print 'VirtualWidth = ' + str(VirtualWidth)
            elif readBannerBytes in [18,19,20,21]:
                VirtualHeight += (int(chunk[cursor].encode('hex'), 16) << ((readBannerBytes - 18) * 8)) >> 0
                print 'VirtualHeight = ' + str(VirtualHeight)
            elif readBannerBytes == 22:
                Orientation = int(chunk[cursor].encode('hex'), 16)*90
                print 'Orientation = ' + str(Orientation)
            elif readBannerBytes == 23:
                Quirks = int(chunk[cursor].encode('hex'), 16)
                print 'Quirks = ' + str(Quirks)
            cursor += 1
            readBannerBytes += 1
            if readBannerBytes == bannerLength:
                # print self.banner.toString()       
                pass
        elif readFrameBytes < 4: #headerbyte
            frameBodylength += int(chunk[cursor].encode('hex'), 16) << (readFrameBytes*8) >> 0
            cursor += 1
            readFrameBytes += 1
        else:
            if length - cursor >= frameBodylength:
                dataBody = dataBody + chunk[cursor : (cursor+frameBodylength)]
                # if bytes_to_int(dataBody[0])!=0xFF or bytes_to_int(dataBody[1])!=0xD8:
                if int(dataBody[0].encode('hex'), 16)!=0xFF or int(dataBody[1].encode('hex'), 16)!=0xD8:
                    continue
                # self.picture.put(dataBody)  
                save_file('D:/doc/trunk/pic.png', dataBody)
                cursor += frameBodylength
                frameBodylength = 0
                readFrameBytes = 0
                dataBody = ""
            else:
                dataBody = dataBody + chunk[cursor:length]
                frameBodylength -= length - cursor;
                readFrameBytes += length - cursor;
                cursor = length;

s.close()