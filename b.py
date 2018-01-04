#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket


TIMEOUT = 15
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(TIMEOUT)

s.connect(('127.0.0.1', 1717))

t = 0
while True:
    reallen = s.recv(4096)
    length = len(reallen)

    if not length:
        continue      
    cursor = 0
    while cursor < length:
        #just do it            
        if readBannerBytes < bannerLength:
            if readBannerBytes==0:
                # self.banner.Version = bytes_to_int(reallen[cursor])                        
            elif readBannerBytes==1:
                # bannerLength = bytes_to_int(reallen[cursor])             
                # self.banner.Length = bannerLength
            elif readBannerBytes in [2,3,4,5]:
                # self.banner.Pid += (bytes_to_int(reallen[cursor]) << ((readBannerBytes - 2) * 8)) >> 0;
            elif readBannerBytes in [6,7,8,9]:
                # self.banner.RealWidth += (bytes_to_int(reallen[cursor]) << ((readBannerBytes - 6) * 8)) >> 0;
            elif readBannerBytes in [10,11,12,13]:
                # self.banner.RealHeight += (bytes_to_int(reallen[cursor]) << ((readBannerBytes - 10) * 8)) >> 0;
            elif readBannerBytes in [14,15,16,17]:
                # self.banner.VirtualWidth += (bytes_to_int(reallen[cursor]) << ((readBannerBytes - 14) * 8)) >> 0;
            elif readBannerBytes in [18,19,20,21]:
                # self.banner.VirtualHeight += (bytes_to_int(reallen[cursor]) << ((readBannerBytes - 18) * 8)) >> 0;
            elif readBannerBytes == 22:
                # self.banner.Orientation = bytes_to_int(reallen[cursor])*90
            elif readBannerBytes == 23:
                # self.banner.Quirks = bytes_to_int(reallen[cursor])
            cursor += 1
            readBannerBytes += 1
            if readBannerBytes == bannerLength:
                print self.banner.toString()                                                    
        elif readFrameBytes < 4:
            frameBodylength =frameBodylength+ ((bytes_to_int(reallen[cursor])<<(readFrameBytes*8)) >> 0)
            cursor += 1
            readFrameBytes += 1
        else:                                                
            if length - cursor >= frameBodylength:                        
                dataBody = dataBody + reallen[cursor:(cursor+frameBodylength)]
                if bytes_to_int(dataBody[0])!=0xFF or bytes_to_int(dataBody[1])!=0xD8:
                    return  
                self.picture.put(dataBody)  
#                         self.save_file('d:/pic.png', dataBody)         
                cursor += frameBodylength
                frameBodylength = 0
                readFrameBytes = 0
                dataBody = ""                    
            else:
                dataBody = dataBody + reallen[cursor:length]                         
                frameBodylength -= length - cursor;
                readFrameBytes += length - cursor;
                cursor = length;
s.close()