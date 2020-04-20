# Placeholder script to give some AP info
from subprocess import Popen, CalledProcessError, check_output, PIPE
import math
import re


def interface_chekcer():
    '''
    Checks for an interface it can use
    
    Returns
    -------
    iface: str
        The name of an interface in string form
    '''

    if_scan = Popen(['ls', '/sys/class/net'], stdout = PIPE)
    if_list = if_scan.communicate()[0].decode('utf-8')
    if_list = if_list.split('\n')
    route_scan = Popen(['netstat', '-rn'], stdout = PIPE)
    route_list = route_scan.communicate()[0].decode('utf-8')

    for iface in if_list:
        try:
            if (iface in route_list):
                if (not 'tun' in iface and not 'lo' in iface):
                    return iface
        except:
            print('No interface found')

def scanWifi(debug, iface):
    '''
    Scans for APs and collects information about them

    Parameters
    ----------
    debug : bool
        A bool to enable or disable debug messages
    iface : str
        a string of the interface to use during scanning

    Returns
    -------
    ap_list
        A list of the found AP(s) SSID
    mac_list
        A list of the found AP(s) MAC Address
    sig_list
        A list of the found AP(s) signal quality and level
    ch_list
        A list of the found AP(s) used channel
    encr_list
        A list of the encryption state of the found AP(s)
    dist_list
        A list of the estimated distance of the found AP(s)

    See Also
    --------
    flipper()   : Flips input into correct order
    distCalc()  : Distance estimate calculation    
    '''

    wifiScan = Popen(['iwlist', iface, 'scan'], stdout= PIPE)
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
    '''
    Flips input into correct order

    Parameters
    ----------
    input_list : list
        A list that contains the raw data of the scanned AP(s)

    Returns
    -------
    ssid
        The SSID of the found AP(s)
    maca
        The MAC Address of the found AP(s)
    sign
        The signal quality and level of the found AP(s)
    chan
        The channel used by the found AP(s)
    encr
        The encryption state of the found AP(s)
    dist
        The estimated distance for the scanner to the AP(s)
    
    See Also
    --------
    distCalc()  : Distance estimate calculation    
    '''
    
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
    '''
    Calculates a rough estimate

    Parameters
    ----------
    sLevel  : str
        The signal Level
    freq    : str
        The frequency used

    Notes
    -----
    The distance calculation is based on Free Space Path Loss (FSPL) and
    is not an accurate way to measure distance from AP(s) as the signal level
    can greatly vary based on a multitude of factors.

    .. math:: Distance = 10 ^ ((27.55 - (20 * log10(frequency)) + signal level) / 20)
    '''
    sLevel = re.sub('[0-9][0-9]/[0-9][0-9]|dBm', '', sLevel)
    freq = (float(freq) * 1000)
    dist = (27.55 - (20 * math.log10(freq)) + abs(float(sLevel))) / 20
    dist = int(pow(10.0, dist))
    distance = str(dist) + 'm'
    return distance

#scanWifi(True)
