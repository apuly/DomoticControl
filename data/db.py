from sqlalchemy import Column, String, BigInteger, Integer, ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base



class DCDatabase(object):
    Base = declarative_base()
    _session = None

    def __init__(self, uri):
        self.uri = uri
        self.engine = create_engine(uri)
        self._session = sessionmaker(bind=self.engine)
        self.Base.metadata.create_all(self.engine)


    class Device(Base):
        __tablename__ = 'device'
        uuid = Column(BigInteger, primary_key = True)
        type = Column(Integer, nullable = False)
        protocol = Column(Integer, nullable = False)

    @property
    def session(self):
        return self._session
