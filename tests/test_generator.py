# Module import 
import pytest

# Project import 
from amore import Generator, Compliment, session

def test_choose_compliment():
    session.add(Compliment(**{"value": "test", "rarity":1}))
    gen = Generator()
    try:
        cmpl = gen.choose_compliment()
    finally:
        session.rollback()
        session.close()
    assert isinstance(cmpl, Compliment)