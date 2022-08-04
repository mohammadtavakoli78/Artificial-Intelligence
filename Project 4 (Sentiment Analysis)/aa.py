import json
import ipaddress
import socket
import threading
import time
from Packet import Packet
from Packet import MessageType

config = None
addressMap = {}
timerMap = {}
serverPort = 67
clientPort = 68

class Config():
    def __init__(self, pool, leaseTime, blackList, reservedList):
        self.pool = pool
        self.leaseTime = leaseTime
        self.blackList = blackList
        self.reservedList = reservedList

def listen():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as serverSocket:
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        serverSocket.bind(("", serverPort))
        while(1):
            data, addr = serverSocket.recvfrom(1024)
            threading.Thread(target=clientHandle, args=(data, serverSocket)).start()

def clientHandle(data, serverSocket):
    packet = Packet().unpack(data)
    clientMacAddress = packet.chaddr
    if packet.flags != 0:
        packet.yiaddr = getNewIp(clientMacAddress)
        packet.flags = 0
        packet.sname = socket.gethostname()
        packet.siaddr = ipaddress.ip_address(socket.gethostbyname(socket.gethostname()))
        packet.options["51"] = int(config.leaseTime)
        serverSocket.sendto(packet.pack(), ('<broadcast>', clientPort))
    else:
        serverSocket.sendto(packet.pack(), ('<broadcast>', clientPort))
        printLog()
    pass

def parseConfigFile():
    with open("config.json") as jsonFile:
        configData = json.load(jsonFile)
        pool = []
        leaseTime = int(configData["lease_time"])
        blackList = configData["black_list"]
        reservedList = configData["reservation_list"]
        if configData["pool_mode"] == "range":
            address = ipaddress.ip_address(configData["range"]["from"])
            pool.append(address)
            while(address != ipaddress.ip_address(configData["range"]["to"])):
                address += 1
                pool.append(address)
        else:
            network = ipaddress.ip_network(configData["subnet"]["ip_block"] + "/" + configData["subnet"]["subnet_mask"])
            for address in network:
                pool.append(address)
        for key, value in reservedList.items():
            if pool.__contains__(value):
                pool.remove(value)
        global config
        config = Config(pool, leaseTime, blackList, reservedList)

def getNewIp(macAddress):
    address = None
    if config.blackList.__contains__(macAddress):
        return ipaddress.ip_address("0.0.0.0")
    elif addressMap.__contains__(macAddress):
        address = addressMap[macAddress]
    elif config.reservedList.__contains__(macAddress):
        address = ipaddress.ip_address(config.reservedList[macAddress])
        config.pool.remove(address)
    else:
        if len(config.pool) != 0:
            address = config.pool.pop()
        else:
            return address
    addressMap[macAddress] = address
    timerMap[macAddress] = config.leaseTime
    return address

def leaseTimer():
    while(1):
        time.sleep(1)
        for macAddress, remainTime in timerMap.copy().items():
            if remainTime == 1:
                timerMap.pop(macAddress)
                config.pool.append(addressMap.pop(macAddress))
            else:
                timerMap[macAddress] = remainTime - 1
            printLog()

def printLog():
    print("--------------------------------------------------------------------------")
    print("MacAddress              IP            RemainingLeaseTime")
    for mac, ip in addressMap.copy().items():
        print(str(mac) + "   " + str(ip) + "         " + str(timerMap[mac]))
    print("--------------------------------------------------------------------------")

if __name__ == "__main__":
    parseConfigFile()
    threading.Thread(target=leaseTimer).start()
    listen()