import dice


class Space:
    """Generic space object that initializes the two attributes shared by all spaces: Name and position on the board."""

    def __init__(self, attrib):

        self.name = attrib['name']            # Property name
        self.position = attrib['position']    # Board position


class Property(Space):
    """Generic property object with the attributes shared by the three space types that can be owned: Streets,
    railroads, and utilities. Inherits attributes from the Space object."""

    def __init__(self, attrib):

        Space.__init__(self, attrib)

        self.monopoly = attrib['monopoly']            # Name of monopoly
        self.monopoly_size = attrib['monopoly_size']  # Number of properties in monopoly
        self.price = attrib['price']                  # Price to buy
        self.price_mortgage = self.price / 2          # Mortgage price
        self.rent = attrib['rent']                    # Initial rent
        self.rent_now = self.rent                     # Current rent
        self.mortgage = False                         # Mortgage status
        self.owner = None                             # Property owner


class Street(Property):
    """Street object that includes attributes related to buildings: cost to build, rent prices at each level of building
    development, and the number of buildings built. Inherits attributes from the Property object."""

    def __init__(self, attrib):

        Property.__init__(self, attrib)

        self.build_cost = attrib['build_cost']        # Building cost
        self.rent_monopoly = self.rent * 2            # Rent with monopoly
        self.rent_house_1 = attrib['rent_house_1']    # Rent with 1 house
        self.rent_house_2 = attrib['rent_house_2']    # Rent with 2 houses
        self.rent_house_3 = attrib['rent_house_3']    # Rent with 3 houses
        self.rent_house_4 = attrib['rent_house_4']    # Rent with 4 houses
        self.rent_hotel = attrib['rent_hotel']        # Rent with hotel
        self.n_buildings = 0                          # Number of buildings

    def get_rent(self):

        return self.rent_now


class Railroad(Property):
    """Railroad object that includes attributes related to rent prices per number of railroads owned. Inherits
    attributes from the Property object."""

    def __init__(self, attrib):

        Property.__init__(self, attrib)

        self.rent_railroad_2 = self.rent * 2  # Rent with 2 railroads
        self.rent_railroad_3 = self.rent * 3  # Rent with 3 railroads
        self.rent_monopoly = self.rent * 4    # Rent with monopoly

    def get_rent(self):

        return self.rent_now


class Utility(Property):
    """Utility object that includes attributes related to rent prices in the Utility monopoly. For this monopoly, rents
    are multipliers of dice rolls rather than absolute values. Inherits attributes from the Property object."""

    def __init__(self, attrib):

        Property.__init__(self, attrib)

        self.rent_monopoly = self.rent + 6

    def get_rent(self):

        d = dice.Dice()
        d.roll()

        return self.rent_now * d.roll_sum


class Tax(Space):
    """Tax object that lists the tax to be paid by a player that lands on a taxed space. Inherits attributes from the
    Space object."""

    def __init__(self, attrib):

        Space.__init__(self, attrib)

        self.tax = attrib['tax']


class Card(object):
    # TODO: Create class
    pass


class Chance(Card):
    # TODO: Create class
    pass


class Chest(Card):
    # TODO: Create class
    pass
