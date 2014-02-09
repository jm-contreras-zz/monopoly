# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 17:32:11 2013

@author: jmcontreras
"""

# Define utility class
class Utility(object):
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.price = 150
        self.rent = 4
        self.rent_now = self.rent
        self.rent_monopoly = 10
        self.mortgage = self.price / 2
        self.owner = None

# Create and fill utilities list
utils = []
utils.append(Utility('Electric Company', 12))
utils.append(Utility('Water Works', 28))