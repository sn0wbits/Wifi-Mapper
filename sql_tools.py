from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class Data(Base):
    __tablename__ = 'MAPPER DATA'
    id = Column('ID', Integer, primary_key=True, unique=True)
    ssid = Column('SSID', String)
    mac = Column('MAC', String)
    sign = Column('QUAL / SIGN', Integer)
    chan = Column('CHANNEL', Integer)
    encr = Column('ENCRYPTED', String)
    lat = Column('LATITUDE', Float)
    lon = Column('LONGITUDE', Float)
    loc = Column('LOCATION', String)

e = create_engine('sqlite:///test.db', echo=False)
Base.metadata.create_all(bind=e)
s = sessionmaker(bind=e)

def wifiTest(ID, SSID, MACaddr, SIGNAL, CHANNEL, ENCRYPTION, LAT, LON):
    session = s()
    t = Data()
    t.id = ID
    t.ssid = SSID
    t.mac = MACaddr
    t.sign = SIGNAL
    t.chan = CHANNEL
    t.encr = ENCRYPTION
    t.lat = LAT
    t.lon = LON
    session.add(t)
    session.commit()
    session.close()
