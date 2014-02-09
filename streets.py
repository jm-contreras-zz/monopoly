# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 17:32:11 2013

@author: jmcontreras
"""

# Define street class
class Street(object):
    def __init__(self, name, position, color, price, rent, rent_build_1,
                 rent_build_2, rent_build_3, rent_build_4, rent_build_5,
                 cost_build):
                     self.name = name
                     self.position = position
                     self.color = color
                     self.price = price
                     self.rent = rent
                     self.rent_now = rent
                     self.rent_monopoly = rent * 2
                     self.rent_build_1 = rent_build_1
                     self.rent_build_2 = rent_build_2
                     self.rent_build_3 = rent_build_3
                     self.rent_build_4 = rent_build_4
                     self.cost_build_5 = rent_build_5
                     self.cost_build = cost_build
                     self.n_building = 0
                     self.mortgage = price / 2
                     self.owner = None

# Read csv file with streets information and create players list
import csv
with open('streets.csv', 'rU') as handle:
    streets_csv = csv.DictReader(handle)
    streets = []
    for s in streets_csv:
        streets.append(Street(s['name'], int(s['position']), s['color'],
                              int(s['price']), int(s['rent']),
                              int(s['rent_build_1']), int(s['rent_build_2']),
                              int(s['rent_build_3']), int(s['rent_build_4']),
                              int(s['rent_build_5']), int(s['cost_build'])))