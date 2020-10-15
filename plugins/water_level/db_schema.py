from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, create_engine, BigInteger
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class DBSchema(object):
    Base = declarative_base()

    _session = None

    def __init__(self, uri):
        self.engine = create_engine(uri)
        self._session = sessionmaker(bind=self.engine)
        self.Base.metadata.create_all(self.engine)

    class GroundWater(Base):
        __tablename__ = 'groundwater'
        time = Column(DateTime, nullable=False, primary_key = True)
        value = Column(Integer, nullable=False)
        sensor = Column(BigInteger, nullable=False)

    @property
    def session(self):
        return self._session
