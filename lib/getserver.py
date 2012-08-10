import os
import sys


def getserver():
	serverconfig = open(os.getcwd()+"\\serverconfig", "rb").readlines()
	return serverconfig

if __name__ == '__main__':
	getserver()