# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */

import unittest

from pyndn import NDN, _pyndn
from threading import Timer
from datetime import datetime

class Basic(unittest.TestCase):

    def test_raiseIfNotConnected (self):

        handle = _pyndn.create()        
        self.assertRaises (_pyndn.NDNError, _pyndn.run, handle, 100) # "ndn_run() should fail when not connected"
        del handle
        
    def test_setRunTimeout (self):
        c = NDN()
        c.run(0)
        
        def change_timeout():
            # print("Changing timeout!")
            c.setRunTimeout(1000)
        
        t = Timer(0.1, change_timeout)
        t.start()
        
        org_start = datetime.now()
        while True:
                self.assertLess ((datetime.now() - org_start).seconds, 3) # setRunTimeout() failed
        
        	start = datetime.now()
        	c.run(5)
        	diff = datetime.now() - start
        
        	if diff.seconds * 1000000 + diff.microseconds > 500000:
        		break
        	# print("working: ", diff)

    def test_ndn_connect_disconnect (self):

        handle = _pyndn.create()

        self.assertRaises (_pyndn.NDNError, _pyndn.disconnect, handle) # "Closing an unopened connection should fail"

        _pyndn.connect(handle)
        _pyndn.disconnect(handle)

        self.assertRaises (_pyndn.NDNError, _pyndn.disconnect, handle) # "Closing handle twice shouldn't work"

        del handle

        c = NDN()
        _pyndn.disconnect (c.ndn_data)
        del c

if __name__ == '__main__':
    unittest.main()
