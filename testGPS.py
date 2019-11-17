from sql_tools import collectGPS
from gps_pos import getGPSPos


c = 0

while True:
    lat, lon, time , alt, speed, track = getGPSPos(False)

    try:
        collectGPS(c, lat, lon)
        c += 1

    except KeyboardInterrupt:
        print('Qutting...')
        exit()
