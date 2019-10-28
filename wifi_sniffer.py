# Placeholder script to give some AP info
from subprocess import Popen, CalledProcessError, check_output, PIPE
import re


def scanWifi(debug):
    wifiScan = Popen(['iwlist', 'wlan0', 'scan'], stdout= PIPE)
    wifiScan2 = Popen(['egrep', 'ESSID|Signal|Address'], stdin = wifiScan.stdout, stdout = PIPE)
    apList = wifiScan2.communicate()[0].decode('utf-8')
    #apList = list(apList.split('                    '))
    apList= list(apList.split('\n'))
    del apList[(len(apList) - 1)]
    apList, sigList, macList = splitter(flipper(apList))
    apList = list(filter(None, apList))
    sigList = list(filter(None, sigList))
    macList = list(filter(None, macList))
    c = 0

    if debug:
        for ap in apList:
            print(ap)
            print(macList[c])
            print(sigList[c])
            c += 1
    else:
        return apList, sigList, macList

def splitter(inputList):
    ssid = [None] * len(inputList)
    sign = [None] * len(inputList)
    maca = [None] * len(inputList)
    counter = 0

    while(counter < len(inputList)):
        if (counter + 2) != len(inputList):
            inputList[counter] = re.sub('                    ESSID:"|"', '', inputList[counter])
            #inputList[counter] = re.sub('\n', '', inputList[counter])
            ssid[counter] = inputList[counter]

        if (counter + 1) != len(inputList):
            inputList[(counter + 1)] = re.sub('          Cell [0-9][0-9] - |Address: ', '', inputList[(counter + 1)])
            #inputList[(counter + 1)] = re.sub ('\n', '', inputList[(counter + 1)])
            maca[counter] = inputList[(counter + 1)]

        inputList[(counter + 2)] = re.sub('                    Quality=|Signal level=', '', inputList[(counter + 2)])
        inputList[(counter + 2)] = re.sub('dBm  ', 'dBm', inputList[(counter + 2)])
        #inputList[(counter + 2)] = re.sub('\n', '', inputList[(counter + 2)])
        sign[counter] = inputList[(counter + 2)]
        counter += 3

    return ssid, sign, maca

def flipper(inputList):
    l = [None] * len(inputList)
    counter = 0

    while(counter < len(inputList)):
        if (counter + 2) != len(inputList):
            l[counter] = inputList[(counter + 2)]

        if (counter + 1) != len(inputList):
            l[(counter + 2)] = inputList[(counter + 1)]
        l[(counter + 1)] = inputList[counter]
        counter += 3

    return l

#scanWifi(True)
