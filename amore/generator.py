# Outer imports
import random
import sys, os
import scipy.stats as scs
from typing import List

# Inner imports
from amore.compliments_db import Compliment, session



class Generator():
    def __init__(self, 
                 distribution: str = "exponential",
                 loc: float = 0, scale: float = 1,
                 *args, **kwargs) -> None:
        
        # Distribution parameters
        self._distribution = distribution
        self._loc = loc
        self._scale = scale

        # Attributes for choice rarity using discrete random variables
        # Could be set up manually through setters
        self.__rarity_list = list()
        self.__norm_probs = list()

        self._ask_db_rarity_list()
        self._rarity_distribution()

    def choose_compliment(self):
        rarity_choice = random.choices(self.__rarity_list, weights=self.__norm_probs, k=1)[0]
        id_list = list()

        stmt = session.query(Compliment.id).\
               filter_by(rarity=rarity_choice).all()
        for i in stmt:
            id_list.append(i)
        
        id_choice = random.choice(id_list)
        cmpl = session.get(Compliment, id_choice)
        return cmpl

    @property
    def rarity_list(self):
        return self.__rarity_list

    @property
    def probs(self):
        return self.__norm_probs

    @rarity_list.setter
    def rarity_list(self, new_rarities: List[int]):
        self.__rarity_list = new_rarities
        self._rarity_distribution()

    @probs.setter
    def probs(self, new_probs: List[int]):
        self.__norm_probs = new_probs

    def _ask_db_rarity_list(self):
        for rarity in session.query(Compliment.rarity).distinct():
            self.__rarity_list.append(rarity[0])

    def _rarity_distribution(self):
        
        # non normalized probabilities
        probs = [self.__compute_prob(i) for i in self.__rarity_list]

        # normalized probabilities
        self.__norm_probs = self.__normalize_probs(probs)

    def __compute_prob(self, value: int):
        if self._distribution == "exponential":
            # lambda = 1/scale
            p = scs.expon.pdf(value, self._loc, self._scale)
        else:
            raise
        return p

    def __normalize_probs(self, probs: List[float]):
        sum0 = sum(probs)
        return [float(i)/float(sum0) for i in probs]



