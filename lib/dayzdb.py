"""DayZ Database Handler"""
import MySQLdb
from parser import CharacterHandler
from getserver import getserver


class DayZDB(object):
    """MYSQL controller."""
    def __init__(self, host, user, pw, db):
        self.db = db
        self.database = MySQLdb.connect(host, user, pw, db)
        self.cursor = self.database.cursor()
        self.tables = self.tablesget()
        self.sql = """"""
        self.characterid = ""
        self.data = ""
        self.player_data = ""

    def tablesget(self):
        """Fetches tables off the database"""
        try:
            self.sql = """SHOW TABLES FROM %s""" % self.db
        except Exception, e:
            raise e
        else:
            return self.execute()

    def Search(self, nick):
        """uses the nick and fetches the table info"""
        try:
            self.sql = """
            SELECT * FROM player_data WHERE PlayerName='%s'
            """ % nick
        except Exception, e:
            raise e
        else:
            self.player_data = self.execute()
            return self.player_data

    def execute(self):
        """General execute statment for SQL"""
        try:
            self.cursor.execute(self.sql)
            data = self.cursor.fetchall()
            self.data = [n for i in data for n in i]
            return self.data
        except Exception, e:
            raise e

    def char_data(self, num=None):
        """Fetches the character data."""
        try:
            if num:
                self.sql = """
                SELECT *  FROM character_data WHERE PlayerID='%s'
                ORDER BY CharacterID DESC LIMIT 1
                """ % num
            else:
                self.sql = """SELECT *  FROM character_data WHERE PlayerID='%s'
                ORDER BY CharacterID DESC LIMIT 1
                """ % self.player_data[0]
        except NameError:
            print "No player selected"
        else:
            return self.execute()

    def player_alive(self):
        """Finds an alive player!"""
        try:
            self.sql = """SELECT * FROM character_data WHERE Alive = 1"""
        except NameError, e:
            raise e
        else:
            return self.execute()

    def character_id(self):
        """Fetches the character ID only."""
        try:
            self.sql = """
            SELECT CharacterID FROM character_data WHERE PlayerID='%s'
            """ % self.player_data[0]
        except Exception:
            print "No characterID's found"
        else:
            self.characterid = self.execute()
            return self.characterid

    def fetch_vehicles(self):
        """Fetches all vehicles on the player which he have ever touched."""
        try:
            itemlist = []
            h = self.character_id()
            for i in h:
                s = [n for n in self.tables if 'object' in n]
                self.sql = """
                SELECT * FROM %s WHERE CharacterID='%s'""" % (s[0], i)
                b = self.execute()
                if b:
                    if len(b) > 11:
                        #intall = len(b) / 11
                        c = [b[i:i + 11] for i in range(0, len(b), 11)]
                        for i in c:
                            itemlist.append(i)
                    else:
                        itemlist.append(b)
        except Exception, e:
            raise e
        else:
            return itemlist

    def save_player(self, player):
        """Saves the player data"""
        try:
            self.sql = """UPDATE character_data SET Inventory=%s, Backpack=%s,
            Worldspace=%s, Medical='[]', Alive=%s, Killsz=%s, HeadshotsZ=%s,
            CurrentState='[]', KillsH=%s, KillsB=%s WHERE CharacterID=%s"""
        except Exception, e:
            raise e
        else:
            player[5] = str(player[5]).replace("'", '"')
            player[6] = CharacterHandler().cencode(player[6])
            player[6] = str(player[6]).replace("'", '"')
            self.cursor.execute(self.sql, (player[5], player[6], player[7],
                player[9], player[13], player[14], player[18], player[20],
                player[0]))
            self.database.commit()

    def save_vehicle(self):
        """Empty"""
        pass

SERVERINFO = getserver()
DAYZDB = DayZDB(SERVERINFO[0], SERVERINFO[1], SERVERINFO[2], SERVERINFO[3])
