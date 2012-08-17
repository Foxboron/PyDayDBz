"""Functions and classes commong to all modules of the script"""
from parser import CharacterHandler
from parser import VehicleHandler
from data import DayZDB
import ast
import os
import json


def health(hp):
    """Display Health."""
    try:
        hp = hp.split(",")
        return hp[7]
    except IndexError:
        return "No info"


def loc(l):
    """Display location."""
    l = ast.literal_eval(l)
    s = "Rot: %s, V/H: %s, O/P: %s" % (str(l[0]), str(l[1][0]), str(l[1][1]))
    return s


class PlayerEdit(object):
    """Main class editing the player variables."""
    inventoryfile = open(os.getcwd() + "\\doc\\inventory", "rb").read()
    toolboxfile = open(os.getcwd() + "\\doc\\toolbox", "rb").read()
    setlist = json.loads(
            open(os.getcwd() + "\\doc\\default", "rb").read())
    teleportloc = json.loads(
            open(os.getcwd() + "\\doc\\teleportlocs", "rb").read())

    def __init__(self, nick, player):
        self.nick = nick
        self.player = player
        self.db = DayZDB
        self.inventory = ast.literal_eval(self.player[5])
        self.backpack = self.player[6]
        self.inventoryfile = open(os.getcwd() + "\\doc\\inventory", "rb").read()
        self.toolboxfile = open(os.getcwd() + "\\doc\\toolbox", "rb").read()
        self.setlist = json.loads(open(os.getcwd() + "\\doc\\default", "rb").read())
        self.teleportloc = json.loads(open(os.getcwd() + "\\doc\\teleportlocs", "rb").read())

    def edit_cords(self, loc):
        """Edit the cords for the character."""
        if loc[0] in self.teleportloc.keys():
            self.player[7] = self.teleportloc[loc[0]]
        else:
            tempt = self.db.Search(loc[0])
            tempdata = self.db.char_data(num=tempt[0])
            self.player[7] = tempdata[7]
        return self.player[7]

    def add_inventory(self, item, *kwargs):
        """Adds an item to the inventory."""
        if item in self.setlist['inventory'].keys():
            self.inventory = json.dumps(self.setlist['inventory'][item])
        else:
            if item in self.inventoryfile:
                self.inventory[1].append(item)
            elif item in self.toolboxfile:
                self.inventory[0].append(item)
            else:
                self.inventory[1].append(item)
        return self.inventory

    def remove_inventory(self, item, *kwargs):
        """Removes and item form the inventory."""
        print self.inventory
        if item in self.inventoryfile:
            self.inventory[1].remove(item)
        elif item in self.toolboxfile:
            self.inventory[0].remove(item)
        return self.inventory

    def add_backpack(self, item, *kwargs):
        """Adds an item to the backpack."""
        if item in self.setlist['backpack'].keys():
            tmp = json.dumps(self.setlist['backpack'][item])
            self.backpack = CharacterHandler().cdecode(tmp)
        else:
            if item in self.toolboxfile:
                if item in self.backpack[1][0][0].keys():
                    self.backpack[1][0][0][item] += 1
                else:
                    self.backpack[1][0][0][item] = 1
            if item in self.inventoryfile:
                if item in self.backpack[1][1][0].keys():
                    self.backpack[1][1][0][item] += 1
                else:
                    self.backpack[1][1][0][item] = 1
        return self.backpack

    def remove_backpack(self, item, *kwargs):
        """Removes an item from the backpack."""
        if item in self.backpack[1][0][0].keys():
            if self.backpack[1][0][0][item] > 1:
                self.backpack[1][0][0][item] -= 1
            else:
                self.backpack[1][0][0].popitem(item)
        if item in self.backpack[1][1][0].keys():
            if self.backpack[1][1][0][item] > 1:
                self.backpack[1][1][0][item] -= 1
            else:
                self.backpack[1][1][0].popitem(item)
        return self.backpack

    def show_inventory(self):
        """Displays the inventory."""
        try:
            self.inventory = ast.literal_eval(self.inventory)
        except ValueError:
            pass
        if self.inventory:
            for i in self.inventory:
                for n in i:
                    if isinstance(n, list):
                        print "%s, x%s" % (n[0], n[1])
                    else:
                        print n
        else:
            print "No inventory"

    def show_backpack(self):
        """Displays the backpack."""
        try:
            self.backpack = CharacterHandler().cdecode(self.backpack)
            if self.backpack[1][0][0].keys() or self.backpack[1][1][0].keys():
                if self.backpack[1][0][0].keys():
                    for k, v in self.backpack[1][0][0].items():
                        print "%s x%s" % (k, v)
                if self.backpack[1][1][0].keys():
                    for k, v in self.backpack[1][1][0].items():
                        print "%s x%s" % (k, v)
            else:
                print "Empty"
        except Exception, e:
            print e
            print "Empty"

    def ShowUser(self, *kwargs):
        """Displays the user information."""
        print ""
        pack = kwargs[0]
        if "info" in pack or not pack:
            print "Nick: %s" % self.nick
            print "Health: %s" % health(self.player[8])
            print "PlayerID: %s" % self.player[1]
            mn = loc(self.player[7])
            print mn
            if self.player[9]:
                print "Player is ALIVE\n"
            else:
                print "Player is DEAD\n"
        if "inventory" in pack or not pack:
            print "_Inventory_"
            self.show_inventory()
        print ""
        if "backpack" in pack or not pack:
            print "_Backpack_"
            self.show_backpack()
        if "storage" in pack or not pack:
            test = self.db.fetch_vehicles()
            if test:
                print "\nStorage info:\n"
                for i in test:
                    print "%s" % i[3]
                    print "CharacterID: %s" % i[5]
                    print  "ObjectID: %s" % i[0]
                    print "ObjectUID: %s" % i[1]
                    print  loc(i[6])
                    print "\nInventory:"
                    VH = VehicleHandler(i[7])
                    inventory, toolbox = VH.vdecode()
                    if inventory.keys() or toolbox.keys():
                        if inventory.keys():
                            for k, v in inventory.items():
                                print "%s x%s" % (k, v)
                        if toolbox.keys():
                            for k, v in toolbox.items():
                                print "%s x%s" % (k, v)
                    else:
                        print "No inventory"
                    print ""
            else:
                print "\nNO storage units!"
