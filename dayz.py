from lib.data import DayZDB
from lib.common import PlayerEdit
from lib.parser import CharacterHandler
import os

class DayZCli(object):
	"""docstring for DayZCli"""
	def __init__(self):
		self.DB = DayZDB
		self.player = ""
		self.character = ""
		self.characterid = []
		self.main()

	def main(self):
		while True:
			s = self.cmd_input(default=True)
			if "user" in s and len(s) == 2:
				self.player = self.DB.Search(s[1])
				if self.player:
					self.character = self.DB.char_data()
					try:
						self.character[6] = CharacterHandler().cdecode(self.character[6])
					except TypeError, e:
						raise e
						pass
					self.PE = PlayerEdit(self.player[1],self.character)
				else:
					print "Character not found!"
			elif "add" in s:
				if self.player:
					if "inventory" in s:
						self.character[5] = self.PE.add_inventory(s[2], s[2:])
					elif "backpack" in s:
						self.character[6] = self.PE.add_backpack(s[2], s[2:])
					else:
						pass
				else:
					print "No selected players!"
			elif "remove" in s:
				if self.player:
						if "inventory" in s:
							self.character[5] = self.PE.remove_inventory(s[2], s[2:])
						elif "backpack" in s:
							self.character[6] = self.PE.remove_backpack(s[2], s[2:])
						else:
							pass
				else:
					print "No selected players!"
			elif "clear" in s:
				if self.player:
					if "inventory" in s:
						self.character[5] = [[],[]]
					elif "backpack" in s:
						self.character[6] = ["DZ_BackPack_EP1",[[],[]],[[],[]]]
				else:
					print "No character selected!"
			elif "print" in s:
				for i in self.character:
					print i
			elif "show" in s:
				if self.character:
					self.PE.ShowUser(s[1:])
				else:
					print "No selected player!"
			elif "save" in s:
				if "vehicle" in s:
					pass
				else:
					self.DB.save_player(self.character)
			elif "ress" in s:
				if len(s) > 1:
					tempt = self.DB.Search(s[1])
					tempdata = self.DB.fetch_char_data(tempt[0])
					tempdata[6] = CharacterHandler().cdecode(tempdata[6])
					tempdata[9] = 1
					self.DB.save_player(tempdata)
				else:
					self.character[9] = 1
			elif "kill" in s:
				if len(s) > 1:
					tempt = self.DB.Search(s[1])
					tempdata = self.DB.fetch_char_data(tempt[0])
					tempdata[9] = 0
					self.DB.save_player(tempdata)
				else:
					self.character[9] = 0
			elif "check" in s:
				try:
					temp = self.DB.Search(s[1])
					if temp:
						temp2 = self.DB.char_data()
						PlayerEdit(s[1],temp2).ShowUser([])
					else:
						print "Character not found!"
				except IndexError, e:
					print "Select a user!"
					raise
			elif "exit" in s:
				exit()
			elif "vehicle" in s:
				pass
			elif "teleport" in s:
				if len(s) > 1:
					pass
				else:
					print "no char selected"
			pass

	def cmd_input(self, message=None, text=None, default=None):
	    if message:
	        print "%s" % message
	    while True:
	        if not text:
	            text = ""
	        data = raw_input("%s>>> " % text)

	        if not data:
	            if default == False:
	                break
	            pass

	        if data:
	            data = data.split(" ")
	            return data

if __name__ == '__main__':
	try:
		Day = DayZCli()
		from lib.invhandler import InventoryHandler
	except KeyboardInterrupt:
		print "\nQuitted"
		exit()


		