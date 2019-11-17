from sql_tools import wifiTest
from wifi_sniffer  import scanWifi
from gps_pos import getGPSPos

def test(debug, count):
    apList, macList, sigList, chList, encrList, distList = scanWifi(False)
    lat, lon, time, alt, speed, track = getGPSPos(False)
    c = 0
    if count is None:
        count = 0

    for ap in apList:
        wifiTest(count, ap, macList[c], sigList[c], chList[c], encrList[c], distList[c], lat, lon)
        c += 1
        count += 1

    if debug:
        print('Done...')

    return count

count = 0

while True:
    try:
        c = test(True, count)
        count = c
    except KeyboardInterrupt:
        exit()
