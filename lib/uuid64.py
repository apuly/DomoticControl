#modified version of library to work with python3.8
#https://github.com/jdowner/uuid64/blob/master/uuid64/uuid64.py
#all credit goes to jdowner

import random
import time

class uuid64():

    def int(self):
        """Return UUID as integer"""
        base = int(time.time()) << 16
        rand = random.SystemRandom().getrandbits(16)
        return base + rand


    def hex(self):
        """Return UUID as hexidecimal"""
        return hex(self.int())[2:-1]


    def bin(self):
        """Return UUID as binary"""
        return bin(self.int())[2:]


    def oct(self):
        """Return UUID as octodecimal"""
        return oct(self.int())[:-1]