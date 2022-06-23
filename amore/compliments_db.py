import os, sys
from requests import session
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from datetime import datetime

project_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = project_dir.replace('/', '\\')

engine = create_engine(f'sqlite:///{project_dir}\\compliments.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base(bind=engine)

class Compliment(Base):
    __tablename__ = 'compliments'

    id = Column(Integer, primary_key=True)
    value = Column(String, nullable=False)
    rarity = Column(Integer, nullable=False)
    date_created = Column(DateTime)
    priority = Column(Integer)
    author = Column(String)
    source = Column(String)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.date_created = datetime.now()

        if 'rarity' not in kwargs.keys():
            self.rarity = 1

        if 'priority' not in kwargs.keys():
            self.priority = 0

        if 'author' not in kwargs.keys():
            self.author = 'DS'

    def __repr__(self):
        return str(self.__dict__)

Base.metadata.create_all(bind=engine)