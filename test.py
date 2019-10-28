from sql_tools import wifiTest
from wifi_sniffer  import scanWifi
from gps_pos import getGPSPos


apList, sigList, macList = scanWifi(False)
lat, lon, time, alt, speed, track = getGPSPos(False)
c = 0

while(c < len(apList)):
    wifiTest(c, apList[c], macList[c], sigList[c], c, True, lat, lon)
    c += 1
