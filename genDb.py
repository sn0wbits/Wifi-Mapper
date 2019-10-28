from sql_tools import wifiTest
import random


c = 0
ap = 'SSID'
encr = True

def randNumb():
    n1 = random.randrange(10, 99, 1)
    n2 = random.randrange(10, 99, 1)
    n3 = random.randrange(10, 99, 1)
    n4 = random.randrange(10, 99, 1)
    n5 = random.randrange(10, 99, 1)
    n6 = random.randrange(10, 99, 1)

    thing = str(n1) + ':' + str(n2) + ':' + str(n3) + ':' + str(n4) + ':' + str(n5) + ':' + str(n6)
    return thing

while(c < 100):
    ssid = ap + str(c)
    mac = randNumb()
    sign = random.randrange(0, 100, 1)
    chan = random.randrange(1, 12, 1)
    lat = 10.7546
    lon = -52.1235

    wifiTest(c, ssid, mac, sign, chan, str(encr), lat, lon)
    c += 1
