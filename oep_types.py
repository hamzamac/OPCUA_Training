"""This is a module template

This module emplate aims at providing a guide in creating standardized 
modules for Simumatik AB
"""

#Module level donders e.g. 
__version__ = ''
__author__ = ''

#Standard library imports
from enum import Enum

#Thirdparty imports
from opcua import ua

#Local imports


#Global varables


#Module members

class Switch():
    ''' '''
    def __init__(self):

        self._type = 0

class OEPTypes(Enum):
    '''The possible tyes OPCUA Emulation Platform'''
    
    SWITCH = Switch()
    LED = 2



        


if __name__ == "__main__":
    t = OEPTypes.SWITCH
    print(t.value)