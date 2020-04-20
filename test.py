from sql_tools import wifiTest
from wifi_sniffer import scanWifi
from gps_pos import getGPSPos
from geopy.geocoders import Nominatim
import os


def test(debug, count):
    ap_list, mac_list, sig_list, ch_list, encr_list, dist_list = scanWifi(False)
    lat, lon, time, alt, speed, track = getGPSPos(False)

    if (count is None):
        count = 0
    for x in range(0, len(ap_list)):
        #loc = getGeoShit(lat, lon)
        wifiTest(count, ap_list[x], mac_list[x], sig_list[x], ch_list[x], encr_list[x], dist_list[x], lat, lon)
        count += 1
    if debug:
        print('Done...')
    return count

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

count = 0

while True:
    try:
        count = test(True, count)
    except KeyboardInterrupt:
        exit()
