# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 17:32:11 2013

@author: jmcontreras
"""

# Define railroad class
class Railroad(object):
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.price = 200
        self.rent = 25
        self.rent_now = self.rent
        self.rent_double = self.rent * 2
        self.rent_triple = self.rent_double * 2
        self.rent_monopoly = self.rent_triple * 2
        self.mortgage = self.price / 2
        self.owner = None

# Create and fill railroads list
rails = []
rails.append(Railroad('Reading Railroad', 5))
rails.append(Railroad('Pennsylvania Railroad', 15))
rails.append(Railroad('B. & 0. Railroad', 25))
rails.append(Railroad('Short Line', 35))