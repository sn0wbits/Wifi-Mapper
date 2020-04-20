from sql_tools import wifiTest
from wifi_sniffer  import scanWifi
from gps_pos import getGPSPos
from geopy.geocoders import Nominatim
import os


def test(debug):
    ap_list, mac_list, sig_list, ch_list, encr_list, dist_list = scanWifi(False)
    lat, lon, time, alt, speed, track = getGPSPos(False)
    for x in range(0, len(ap_list)):
        #loc = getGeoShit(lat, lon)
        wifiTest(x, ap_list[x], mac_list[x], sig_list[x], ch_list[cx, encr_list[x], dist_list[x], lat, lon)
    if debug:
        print('Done...')
    return len(ap_list)

def getGeoShit(lat, lon):
    lang = "en_US" # Change this to the language you wish to use
    geolocator = Nominatim(user_agent='wifi-mapper')
    location = geolocator.reverse(str(lat) + ', ' + str(lon), language=lang)
    address = location.raw['address']

    if 'city_district' in address:
        city = address.get('city_district', 'N/A')
    else:
        city = address.get('city', 'N/A')

    state = address.get('state', 'N/A')
    country = address.get('country', 'N/A')

    result_s = city + ', ' + state + ', ' + country

    return result_s

while True:
    try:
        test(True)
    except KeyboardInterrupt:
        exit()
