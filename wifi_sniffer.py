# Placeholder script to give some AP info
from subprocess import Popen, CalledProcessError, check_output, PIPE
import math
import re

# Scans for APs, sends to flipper then either prints or returns
def scanWifi(debug):
    wifiScan = Popen(['iwlist', 'wlan0', 'scan'], stdout= PIPE)
    wifiScan2 = Popen(['egrep', 'ESSID|Signal|Address|Channel|Encryption key'], stdin = wifiScan.stdout, stdout = PIPE)
    apList = wifiScan2.communicate()[0].decode('utf-8')
    apList= list(apList.split('\n'))
    del apList[(len(apList) - 1)]
    apList, macList, sigList, chList, encrList, distList = flipper(apList)

    if debug:
        c = 0
        for ap in apList:
            print(ap)
            print('-'*20)
            print(macList[c])
            print('.'*20)
            print(sigList[c])
            print('-'*20)
            print(chList[c])
            print('-'*20)
            print(encrList[c])
            print('-'*20)
            print(distList[c])
            print('.'*20)
            c += 1
    else:
        return apList, macList, sigList, chList, encrList, distList

# Flips input based on substrings then calculates distance and returns
def flipper(inputList):
    ssid = [None] * (len(inputList) + 10)
    maca = [None] * (len(inputList) + 10)
    sign = [None] * (len(inputList) + 10)
    chan = [None] * (len(inputList) + 10)
    encr = [None] * (len(inputList) + 10)
    freq = [None] * (len(inputList) + 10)
    dist = [None] * (len(inputList) + 10)
    counter = 0

    for x in inputList:
        if 'ESSID' in  x:
            x = re.sub('                    ESSID:"|"', '', x)
            ssid[counter] = x
        elif 'Address:' in x:
            x = re.sub('          Cell [0-9][0-9] - Address: ', '', x)
            maca[counter] = x
        elif 'Signal' in x:
            x = re.sub('                    Quality=|Signal level=', '', x)
            sign[counter] = x
        elif 'Channel:' in x:
            x = re.sub('                    Channel:', '', x)
            chan[counter] = x
        elif 'Encryption' in x:
            x = re.sub('                    Encryption key:|', '', x)
            encr[counter] = x
        else:
            x = re.sub('                    Frequency:| .*', '', x)
            freq[counter] = x
        counter += 1

    ssid = list(filter(None, ssid))
    maca = list(filter(None, maca))
    sign = list(filter(None, sign))
    chan = list(filter(None, chan))
    encr = list(filter(None, encr))
    freq = list(filter(None, freq))

    counter = 0

    for f in freq:
        dist[counter] = distCalc(sign[counter], f)
        counter += 1
    dist = list(filter(None, dist))

    return ssid, maca, sign, chan, encr, dist

# Calculates a rough estimate based on the signal level and frequency
def distCalc(sLevel, freq):
    sLevel = re.sub('[0-9][0-9]/[0-9][0-9]|dBm', '', sLevel)
    freq = (float(freq) * 1000)
    dist = (27.55 - (20 * math.log10(freq)) + abs(float(sLevel))) / 20
    dist = int(pow(10.0, dist))
    distance = str(dist) + 'm'

    return distance


#scanWifi(True)
