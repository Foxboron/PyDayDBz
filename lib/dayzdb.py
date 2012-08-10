import MySQLdb
import os
from collections import OrderedDict
from parser import CharacterHandler
from getserver import getserver

# class DayZ(object):
#   """MYSQL controller."""
#   def __init__(self, host, user, pw, db):
#       self.db = db
#       self.database = MySQLdb.connect(host, user, pw, db)
#       self.cursor = self.database.cursor()

#   def tables(self):
#       try:
#           sql = """SHOW TABLES FROM %s""" % (self.db)
#           self.cursor.execute(sql)
#           self.tables=[element[0] for element in self.cursor.fetchall()]
#           return self.tables
#       except:
#           print "Failed fetching tables"
#           raise

#   def Search(self, name):
#       try:
#           sql = """SELECT * FROM player_data WHERE PlayerName='%s'""" % name
#           self.cursor.execute(sql)
#           self.player_data = [i for element in self.cursor.fetchall() for i in element]
#           return self.player_data
#       except Exception, e:
#           raise e

#   def char_data(self):
#       try:
#           sql = """SELECT * FROM character_data WHERE PlayerID=%s""" % self.player_data[0]
#           self.cursor.execute(sql)
#           self.character_data = [n for i in self.cursor.fetchall() for n in i]
#           return self.character_data
#       except Exception, e:
#           raise e

#   def player_alive(self):
#       try:
#           sql = """SELECT * FROM character_data WHERE Alive = 1"""
#           self.cursor.execute

class DayZDB(object):
    """MYSQL controller."""
    def __init__(self, host, user, pw, db):
        self.db = db
        self.database = MySQLdb.connect(host, user, pw, db)
        self.cursor = self.database.cursor()
        self.tables = self.tablesget() 


    def tablesget(self):
        try:
            self.sql = """SHOW TABLES FROM %s""" % self.db
        except Exception, e:
            raise e
        else:
            return self.execute()

    def Search(self, nick):
        try:
            self.sql = """SELECT * FROM player_data WHERE PlayerName='%s'""" % nick
        except Exception, e:
            raise e
        else:
            self.player_data = self.execute()
            return self.player_data

    def execute(self):
        try:
            self.cursor.execute(self.sql)
            data = self.cursor.fetchall()
            self.data = [n for i in data for n in i]
            return self.data
        except Exception, e:
            raise e

    def char_data(self):
        try:
            self.sql = """SELECT *  FROM character_data WHERE PlayerID='%s' ORDER BY CharacterID DESC LIMIT 1""" % self.player_data[0]
        except NameError:
            print "No player selected"
        else:
            return self.execute()

    def fetch_char_data(self,ID):
        try:
            self.sql = """SELECT *  FROM character_data WHERE PlayerID='%s' ORDER BY CharacterID DESC LIMIT 1""" % ID
        except NameError:
            print "No player selected"
        else:
            return self.execute()

    def player_alive(self):
        try:
            sql = """SELECT * FROM character_data WHERE Alive = 1"""
        except NameError, e:
            raise e
        else:
            return self.execute()

    def character_id(self):
        try:
            self.sql = """SELECT CharacterID FROM character_data WHERE PlayerID='%s'""" % self.player_data[0]
        except Exception, e:
            print "No characterID's found"
        else:
            self.characterid = self.execute()
            return self.characterid

    def fetch_vehicles(self):
        try:
            itemlist = []
            h = self.character_id()
            for i in h:
                s = [n for n in self.tables if 'object' in n]
                self.sql = """SELECT * FROM %s WHERE CharacterID='%s'""" % (s[0], i)
                b = self.execute()
                if b:
                    if len(b) > 11:
                        intall = len(b) / 11
                        c = [b[i:i+11] for i in range(0, len(b), 11)]
                        for i in c:
                            itemlist.append(i)
                    else:
                        itemlist.append(b)
        except Exception, e:
            raise e
        else:
            return itemlist

    def save_player(self, player):
        try:
            #ini = OrderedDict(zip(l,player[7:]))
            self.sql = """UPDATE character_data SET Inventory=%s, Backpack=%s, Worldspace=%s, Medical='[]', Alive=%s, Killsz=%s, HeadshotsZ=%s, CurrentState='[]', KillsH=%s, KillsB=%s WHERE CharacterID=%s"""
            #self.sql = """INSERT INTO character_data(Inventory, Backpack, Worldspace, Medical, Alive, Killsz , HeadshotsZ , CurrentState, KillsH , KillsB)  VALUES('%s','%s','%s','%s',%s,%s,%s,'%s',%s,%s) WHERE PlayerID = %s""" % (player[5], player[6],player[7], player[8], player[9],player[13],player[14],player[17],player[18], player[20]) 
        except Exception, e:
            raise e
        else:
            #(player[5],player[6],player[7],player[9],player[13],player[14],player[17],player[18],player[20],player[1])
            player[5] = str(player[5]).replace("'",'"')
            player[6] = CharacterHandler().cencode(player[6])
            player[6] = str(player[6]).replace("'",'"')
            self.cursor.execute(self.sql,(player[5],player[6],player[7],player[9],player[13],player[14],player[18],player[20],player[0]))
            self.database.commit()

    def save_vehicle(self):
        pass

#DAYZDB = DayZDB("141.0.137.20", "wk", "asdf1234", "dayzed")
serverinfo = getserver()
DAYZDB = DayZDB(serverinfo[0], serverinfo[1], serverinfo[2], serverinfo[3])