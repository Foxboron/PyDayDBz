"""Serverconfig file handler"""
import os


def getserver():
    """Fetches the server config file."""
    serverconfig = open(os.getcwd() + "\\serverconfig", "rb")
    serverconfig = serverconfig.read().split('\r\n')
    return serverconfig

if __name__ == '__main__':
    getserver()
