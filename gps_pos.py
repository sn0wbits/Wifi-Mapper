import gps


def getGPSPos(debug):
    s = gps.gps('localhost', '2947')
    s.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    conn = False

    while(not conn):
        try:
            posRep = s.next()
            if posRep['class'] == 'TPV':
                if hasattr(posRep, 'time') and hasattr(posRep, 'lat') and hasattr(posRep, 'lon') and hasattr(posRep, 'alt') and hasattr(posRep, 'speed') and hasattr(posRep, 'track'):
                    if debug:
                        print(10*'-' + ' DEBUG ' + 10*'-')
                        print('TIME:........{}'.format(posRep.time))
                        print('LATITUDE:....{}\nLONGITUDE:...{}\n'.format(posRep.lat, posRep.lon))
                        print('ALTITUDE:....{} M\nSPEED:.......{} M/S'.format(posRep.alt, posRep.speed))
                        print('TRACK:.......{}'.format(posRep.track))
                        conn = True
                    else:
                        if posRep.lat is None:
                            pass
                        if posRep.lon is None:
                            pass
                        return posRep.lat, posRep.lon, posRep.time, posRep.alt, posRep.speed, posRep.track

        except KeyboardInterrupt:
            quit()
        except StopIteration:
            s = None
            print('TERMINATED')

#getGPSPos(True)
