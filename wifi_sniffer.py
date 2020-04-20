# Placeholder script to give some AP info
from subprocess import Popen, CalledProcessError, check_output, PIPE
import math
import re


# Scans for APs, sends to flipper then either prints or returns
def scanWifi(debug):
    wifiScan = Popen(['iwlist', 'wlan0', 'scan'], stdout= PIPE)
    wifiScan2 = Popen(['egrep', 'ESSID|Signal|Address|Channel|Encryption key'], stdin = wifiScan.stdout, stdout = PIPE)
    ap_list = wifiScan2.communicate()[0].decode('utf-8')
    ap_list= list(ap_list.split('\n'))
    del ap_list[(len(ap_list) - 1)]
    ap_list, mac_list, sig_list, ch_list, encr_list, dist_list = flipper(ap_list)

    if debug:
        c = 0
        for x in range(0, len(ap_list)):
            print(f'{ap_list[x]}\n{"-"*20}\n{mac_list[x]}\n{"."*20}\n' + \
            f'{sig_list[x]}\n{"-"*20}\n{ch_list[x]}\n{"-"*20}\n' + \
            f'{encr_list[x]}\n{"-"*20}\n{dist_list[x]}\n{"."*20}')
    else:
        return ap_list, mac_list, sig_list, ch_list, encr_list, dist_list

# Flips input based on substrings then calculates distance and returns
def flipper(input_list):
    ssid = [None] * (len(input_list) + 10)
    maca = [None] * (len(input_list) + 10)
    sign = [None] * (len(input_list) + 10)
    chan = [None] * (len(input_list) + 10)
    encr = [None] * (len(input_list) + 10)
    freq = [None] * (len(input_list) + 10)
    dist = [None] * (len(input_list) + 10)
    counter = 0

    for x in input_list:
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
    counter = 0

    ssid = list(filter(None, ssid))
    maca = list(filter(None, maca))
    sign = list(filter(None, sign))
    chan = list(filter(None, chan))
    encr = list(filter(None, encr))
    freq = list(filter(None, freq))

    for x in range(0, len(freq)):
        dist[x] = distCalc(sign[x], freq[x])

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
