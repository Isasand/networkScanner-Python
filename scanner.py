from ftplib import FTP
import ping
from socket import *
import ports
#import paramiko

connected_devices = []

for i in range(1,254):
        ip = "192.168.0." + str(i)
        ans = str(ping.quiet_ping(ip, 0.003, 1))
        #print(ans(0))
        if ans[1] == "0":
                connected_devices.append(ip)

print("connected devices: ")
for adress in connected_devices:
        print(adress)
print("\n")

def scancommonports(address):
        common_ports = ports.listofports
        for p in common_ports:
                scanport(address,p.port)

def scancommonportsfromlist(iplist):
        for address in iplist:
                scancommonports(address)

def scanport(address, port):
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(0.3)
        result = s.connect_ex((address, port))
        if result == 0:
                print("Port %s open on %s" %(port, address))
        s.close()

def scanportsfromlist(iplist):
        for address in iplist:
                for i in range(0,1024):
                        scanport(address, i)


def getHTTPport(socket, address, port):
        data = ""
        CRLF = "\r\n\r\n"
        print("Content of port %s on ip %s:" %(port, address))
        socket.send("GET / HTTP/1.0%s" %(CRLF) )
        if port == 3306:
                data = (socket.recv(1000000))
        else:
                data = (socket.recv(1000000))
        print(data)
        socket.shutdown(1)



def scanHTTPport(iplist):
        for address in iplist:
                for port in [80,8080, 3124, 443]:
                        s = socket(AF_INET, SOCK_STREAM)
                        s.settimeout(0.5)
                        res = s.connect_ex((address, port))
                        if res == 0:
                                getHTTPport(s, address, port)
                        s.close()

def scanFTPport(iplist):
        for address in iplist:
                for i in range(989, 990):
                        scanport(address, i)
                for port in [20,21]:
                        #scanport(address,port)
                        s = socket(AF_INET, SOCK_STREAM)
                        s.settimeout(0.5)
                        res = s.connect_ex((address, port))
                        if res == 0:
                                ans = input("FTP port %s open on ip %s, press 1 to attempt login\n" %(port, address))
                                if ans == 1:
                                        loginFTP(address)

def loginFTP(ip):
        ftp = FTP(ip)
        print("Connecting...")
        ftp.login("pi", "raspberry")
        print("\n**WELCOME**\n\n" )
        ftp.retrlines('LIST')
        file = raw_input("\n\nchoose a file to rename: ")
        newname = raw_input("Input new name: ")
        ftp.rename(file,newname)
        ftp.retrlines('LIST')

def scanSSHport(iplist):
        for address in iplist:
                s = socket(AF_INET, SOCK_STREAM)
                s.settimeout(0.5)
                res = s.connect_ex((address, 22))
                if res == 0:
                        ans = input("SSH port open on ip %s" %address)


#scanSSHport(connected_devices)
#scanportsfromlist(connected_devices)
scanFTPport(connected_devices)
#scanHTTPport(connected_devices)
#scancommonportsfromlist(connected_devices)

print("scan done")

