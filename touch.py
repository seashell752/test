#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys
import time


TIMEOUT = 15
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(TIMEOUT)

s.connect(('127.0.0.1', 1111))
reply = s.recv(1024)
print reply
restr = reply.split()
print restr
version = restr[1]
max_contacts = int(restr[3])
max_x = int(restr[4])
max_y = int(restr[5])
max_pressure = int(restr[6])
pid = int(restr[8])
print version, max_contacts, max_x, max_y, max_pressure, pid

def convert(x, y):
    return(x*1080/max_x, y*1920/max_y)

while True:
       x_str = raw_input("x:")
       y_str = raw_input("y:")
       x = int(x_str)
       y = int(y_str)
       print x, y
       x, y = convert(x, y)
       print x, y
       cmd = 'd 0 {} {} 50 \n'.format(x,y)
       print cmd
       s.sendall(cmd)
       s.sendall('c\n')
       time.sleep(2)
       s.sendall('u 0\n')
       s.sendall('c\n')
s.close()
