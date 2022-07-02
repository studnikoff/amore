import os, sys
import logging
from typing import Type
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import create_engine
from sqlalchemy import select, update
from datetime import datetime

# Logging configuration
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s]  %(name)s  %(levelname)s: %(message)s',
                    filename='data/amore.log')
# Absolute path of project directory
project_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = project_dir.replace('/', '\\')

# Controling environment variables configuration for db
def get_environ(key: str, default_value: str) -> str:
    """Функция для возвращения значения из переменной окуржения

    Args:
        key (str): Ключ переменной окружения, 
        по которому получаем значение.

        default_value (str): Значение по умолчанию, 
        если ключ отсутствует в переменной окружения 

    Returns:
        str: Значение переменной окружения для конфигурации БД
    """    
    if key in os.environ.keys():
        name = os.environ[key]
    else:
        name = default_value
    return name

# Database configuration
db = get_environ('AMORE_DB', 'sqlite')
if db == 'sqlite':
    # Windows sqlite
    engine = create_engine(f'sqlite:///data/compliments.db', echo=True)
elif db == 'postgres':
    user = get_environ('POSTGRES_USER', 'postgres')
    password = get_environ('POSTGRES_PASSWORD', '1343')
    hostname = get_environ('POSTGRES_ADDR', 'localhost')
    port = get_environ('POSTGRES_PORT', '5432')
    dbname = get_environ('POSTGRES_DB', 'db')
    engine = create_engine(f'postgresql://{user}:{password}@{hostname}:{port}/{dbname}', echo=True)


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
    used = Column(Boolean)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.date_created = datetime.now()

        if 'rarity' not in kwargs.keys():
            self.rarity = 1

        if 'priority' not in kwargs.keys():
            self.priority = 0

        if 'author' not in kwargs.keys():
            self.author = 'DS'

        self.__verify()

    def __repr__(self):
        length = 40
        if len(self.value) <= length:
            val = self.value
        else:
            val = self.value[:length] + '<...>'
        res = f'Id: {self.id}, value: {val}, rarity: {self.rarity} ({self.date_created})'
        return res

    def __verify(self):
        def verify(attr: str, type: Type):
            if attr in self.__dict__.keys():
                if isinstance(getattr(self, attr), type):
                    pass
                else:
                    raise TypeError(f"Wrong attribute type. Attribute {attr} is {type}")
        
        def list_verify(l: list, type: Type):
            for i in l:
                verify(i, type)

        int_attr = ["id", "rarity", "priority"]
        list_verify(int_attr, int)

        str_attr = ["value", "author", "source"]
        list_verify(str_attr, str)

        date_attr = ["date_created"]
        list_verify(date_attr, datetime)

        bool_attr = ["used"]
        list_verify(bool_attr, bool)

        

Base.metadata.create_all(bind=engine)

def add_compliment(value: str, rarity: int, **kwargs):
    """Adding compliment into database

    Args:
        value (str): Text of compliment
        rarity (int): Rarity of compliment (more rare, less often should be returned)
    """    
    try:
        cmpl = Compliment(value=value, rarity=rarity, **kwargs)
        session.add(cmpl)
    except:
        logging.exception("Adding compliment exception into database")
        logging.warning("Adding only value and rarity, everything else is default")
        cmpl = Compliment(value=value, rarity=rarity)
        session.add(cmpl)
    finally:
        logging.debug(f"Added compliment into database: {cmpl}")
        session.commit()

def get_compliment(id: int) -> Type[Compliment]:
    """Getting compliment instance by its id

    Args:
        id (int): compliment id in database

    Returns:
        Type[Compliment]: compliment class instance
    """    
    cmpl = session.get(Compliment, id)
    return cmpl

def search_compliment() -> Type[Compliment]:
    # TODO: for searching compliment by other attributes except id
    pass

def edit_compliment(id: int, changes: dict) -> None:
    cmpl = session.get(Compliment, id)
    print(cmpl)
    for key in changes.keys():
        print(key)
        if hasattr(cmpl, key):
            setattr(cmpl, key, changes[key])
        else:
            raise AttributeError(f"Compliment {cmpl} does not have attribute {key}")
    session.commit()