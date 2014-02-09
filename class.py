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




#http://stackoverflow.com/questions/2468334/python-how-to-create-dynamic-and-expandable-dictionaries

## Define property class
#class Property(object):
#    def __init__(self, name, position, price, rent_now, rent_single,
#                 rent_monopoly, mortgage, owner):
#        self.name = name
#        self.position = position
#        self.price = price
#        self.rent_now = rent_now
#        self.rent_single = rent_single
#        self.rent_monopoly = rent_monopoly
#        self.mortgage = mortgage
#        self.owner = 0
#
## Define street class
#class Street(Property):
#    def __init__(self, color, rent_house_1, rent_house_2, rent_house_3,
#                 rent_house_4, rent_hotel, cost_house, cost_hotel):
#        self.color = color
#        self.rent_house_1 = rent_house_1
#        self.rent_house_2 = rent_house_2
#        self.rent_house_3 = rent_house_3
#        self.rent_house_4 = rent_house_4
#        self.rent_hotel = rent_hotel
#        self.cost_house = cost_house
#        self.cost_hotel = cost_hotel
#
## Define utility class
#class Utility(Property):
#    def __init__(self):
#        self.price = 150
#        self.rent_single = 4
#        self.rent_monopoly = 10
#        self.mortgage = 75
#
## Define railroad class
#class Railroad(Property):
#    def __init__(self):
#        self.price = 200
#        self.rent_single = 25       # Rent with 1 railroad
#        self.rent_double = 50       # Rent with 2 railroads
#        self.rent_triple = 100      # Rent with 3 railroads
#        self.rent_monopoly = 200    # Rent with 4 railroads
#        self.mortgage = 100