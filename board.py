# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 13:01:19 2013

@author: jmcontreras
"""

# Create a board
import csv
with open('board.csv', 'rU') as handle:
    board_csv = csv.DictReader(handle)
    board = []
    for b in board_csv:
        
        # Properties
        if b['type'] == 'street':
            board.append(Street(b['name'], int(b['position']), b['color'],
                                int(b['price']), int(b['rent']),
                                int(b['rent_build_1']), int(b['rent_build_2']),
                                int(b['rent_build_3']), int(b['rent_build_4']),
                                int(b['rent_build_5']), int(b['cost_build'])))            
        elif b['type'] == 'railroad':
            board.append(Railroad(b['name'], int(b['position'])))
        elif b['type'] == 'utility':
            board.append(Utility(b['name'], int(b['position'])))
        
        # Tax
        elif b['type'] == 'tax':
            board.append(Tax(b['name'], int(b['position']), int(b['price'])))
        
        # Other
        else:
            board.append(Space(b['name'], int(b['position'])))



class Tax(object):
    def __init__(self, name, position, price):
        self.name = name
        self.position = position
        self.price = price

class Space(object):
    def __init__(self, name, position):
        self.name = name
        self.position = position