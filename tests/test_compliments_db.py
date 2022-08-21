# Module import 
import pytest
import os

# Project import 
from amore.compliments_db import get_environ, session
from amore.compliments_db import Compliment
from amore.compliments_db import add_compliment, get_compliment, edit_compliment


def test_get_environ():
    path_test = os.environ['PATH']
    path_result = get_environ('PATH', 'ERROR')

    assert path_test == path_result


@pytest.fixture
def record1():
    test1 = {
        'value': 'You are beautiful!',
        'rarity': 100
    }
    return test1


@pytest.fixture
def record2():
    test2 = {
        'value': 'Soul is infinite',
        'rarity': 0,
        'priority': 2,
        'author': 'DS',
        'source': 'test'
    }
    return test2

def test_orm_verification():
    with pytest.raises(TypeError):
        Compliment(id='figure', value=42, rarity='rare', priority='very')


def test_db_write(record1, record2):
    session.query(Compliment).delete()

    cmpl1 = Compliment(**record1)
    cmpl2 = Compliment(**record2)

    session.add_all([cmpl1, cmpl2])
    session.commit()

    db_result = [i for i in session.query(Compliment).all()]
    session.query(Compliment).delete()
    session.commit()

    assert True

def test_add_compliment(record1, record2):
    session.query(Compliment).delete()

    add_compliment(**record1)
    add_compliment(**record2)

    query = session.query(Compliment).all()


    assert True

def test_get_compliment(record1):
    session.query(Compliment).delete()

    cmpl1 = Compliment(**record1)
    session.add(cmpl1)
    session.commit()

    res = get_compliment(cmpl1.id)

    assert res == cmpl1

def test_edit_compliment(record1):
    session.query(Compliment).delete()

    cmpl1 = Compliment(**record1)
    session.add(cmpl1)
    session.commit()

    cmpl1 = session.query(Compliment).filter_by(value=record1['value']).all()[0]
    print(cmpl1)
    edit_compliment(cmpl1.id, {'value': 'test_edit_compliment'})

    res = session.get(Compliment, cmpl1.id)

    session.query(Compliment).delete()
    assert res.value == 'test_edit_compliment'