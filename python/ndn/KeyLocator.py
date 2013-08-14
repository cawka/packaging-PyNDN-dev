## -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-
#
# Copyright (c) 2011-2013, Regents of the University of California
# BSD license, See the COPYING file for more information
# Written by: Derek Kulinski <takeda@takeda.tk>
#             Jeff Burke <jburke@ucla.edu>
#             Alexander Afanasyev <alexander.afanasyev@ucla.edu>
#

import _pyndn
from Name import Name

class KeyLocator (object):
    __slots__ = ["ndn_data", "keyName"]
    
    def __init__ (self, keyName = None):
        if isinstance (keyName, Name):
            self.keyName = keyName
        else:
            self.keyName = Name (keyName)

        self.ndn_data = None

    @staticmethod
    def getDefault ():
        return KeyLocator (_pyndn.get_default_key_name ())

    def __setattr__ (self, name, value):
        if name != "ndn_data":
            object.__setattr__ (self, 'ndn_data', None)

        object.__setattr__(self, name, value)

    def __getattribute__ (self, name):
        if name=="ndn_data":
            if not object.__getattribute__ (self, 'ndn_data'):
                self.ndn_data = _pyndn.KeyLocator_to_ndn (name = self.keyName.ndn_data)
                
        return object.__getattribute__(self, name)

    def __repr__ (self):
        return "ndn.KeyLocator(%s)" % self.keyName
    
