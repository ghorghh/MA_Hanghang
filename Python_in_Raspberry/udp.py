#Class UDP
import socket
import struct
import logging
import time

class myudp:
    def __init__(self, serverName, serverPort, timeout):
        self.serverName = serverName
        self.serverPort = serverPort
        self.timeout = timeout

    def start(self):
        client1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client1.bind(('192.168.137.50', 9999))
        ##client1.connect((self.serverName, self.serverPort))
##        client1.settimeout(self.timeout)#second
        return client1
    
    def udp_manipulation(self,client1):
        data, addr = client1.recvfrom(1024)
##        print(data)
        data_struct = struct.unpack('11B6?3B', data)
##        print(data_struct, type(data_struct))
            
        return data_struct
