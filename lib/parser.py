"""Parsing character and vehicle from the standar DayZ value into something
    python understand"""
from collections import OrderedDict
import ast


class CharacterHandler(object):
    """Handles the data inside the character."""
    def cencode(self, backpack):
        """Encodes a dict back to the original structure for DayZ."""
        self.backpack = backpack
        #print self.backpack
        try:
            toolbox = [i for i in self.backpack[1][0][0].keys()]
            toolboxc = [i for i in self.backpack[1][0][0].values()]
            backpack = [i for i in self.backpack[1][1][0].keys()]
            backpackc = [i for i in self.backpack[1][1][0].values()]
            self.backpack = [
                            "DZ_Backpack_EP1",
                            [toolbox, toolboxc],
                            [backpack, backpackc]
                            ]
        except AttributeError:
            raise
        return self.backpack

    def cdecode(self, backpack):
        """Decodes the dict inside the DayZ DB for python using OrderedDict."""
        try:
            self.backpack = ast.literal_eval(backpack)
        except:
            self.backpack = backpack
        try:
            self.toolbox = OrderedDict(zip(self.backpack[1][0],
                                           self.backpack[1][1]))
        except:
            self.toolbox = OrderedDict()
        try:
            self.backpack = [self.backpack[0],
            [
            [OrderedDict(zip(self.backpack[1][0], self.backpack[1][1]))],
            [OrderedDict(zip(self.backpack[2][0], self.backpack[2][1]))]
            ]
            ]
        except Exception:
            pass
        return self.backpack


class VehicleHandler(object):
    """Nothing."""
    def __init__(self, inventory):
        self.character = ast.literal_eval(inventory)

    def vencode(self):
        """Nothing."""
        toolbox = [i for i in self.toolbox.keys()]
        toolboxc = [i for i in self.toolbox.values()]
        inventory = [i for i in self.inventory.keys()]
        inventoryc = [i for i in self.inventory.values()]
        backpack = []
        backpackc = []
        self.inventory = [
                            [toolbox, toolboxc],
                            [inventory, inventoryc],
                            [backpack, backpackc]]
        return self.inventory

    def vdecode(self):
        """Nothing."""
        try:
            self.toolbox = OrderedDict(zip(
                                            self.character[0][0],
                                            self.character[0][1]))
        except:
            self.toolbox = {}
        try:
            self.inventory = OrderedDict(zip(
                                                self.character[1][0],
                                                self.character[1][1]))
        except:
            self.inventory = {}
        return (self.toolbox, self.inventory)
        #print self.toolbox
        #print self.inventory
        #print self.backpack
