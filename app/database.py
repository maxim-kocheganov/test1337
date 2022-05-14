from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric
import random
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import func
from app.settings import SQLALCHEMY_DATABASE_URL

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://admin3:pass@192.168.0.102/test3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

Base = declarative_base()

class Endpoint(Base):
    __tablename__ = "endpoints"    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item = relationship("Item")

class Item(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    dev_types = [ "emeter", "zigbee", "lora", "gsm"]
    dev_type = Column(String)
    dev_id = Column(String)
    endpoint_id = Column(Integer, ForeignKey('endpoints.id'))
    def setRandType(self):
        rnd = random.randint(0,len(self.dev_types) - 1)
        self.dev_type = self.dev_types[rnd]
    def setRandId(self):
        self.dev_id = "%02x:%02x:%02x:%02x:%02x:%02x" % (random.randint(0, 255),
                             random.randint(0, 255),
                             random.randint(0, 255),
                             random.randint(0, 255),
                             random.randint(0, 255),
                             random.randint(0, 255))

Base.metadata.create_all(engine)