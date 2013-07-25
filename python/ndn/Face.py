## -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-
#
# Copyright (c) 2011, Regents of the University of California
# BSD license, See the COPYING file for more information
# Written by: Derek Kulinski <takeda@takeda.tk>
#             Jeff Burke <jburke@ucla.edu>
#             Alexander Afanasyev <alexander.afanasyev@ucla.edu>
#

import _ndn

import Closure
import Interest
from Name import Name

import threading

class Face (object):
    """
    Class that provides interface to connect to the underlying NDN daemon
    """
    
    def __init__(self):
        self._handle_lock = threading.Lock()
		self.ndn_data = _pyndn.create()
        self.connect ()

    def connect (self):
		_pyndn.connect(self.ndn_data)

    def disconnect (self):
		_pyndn.disconnect(self.ndn_data)

    def defer_verification (self, deferVerification = True):
                _pyndn.defer_verification(self.ndn_data, 1 if deferVerification else 0)

    def _acquire_lock(self, tag):
		if not _pyndn.is_run_executing(self.ndn_data):
#			print("%s: acquiring lock" % tag)
            self._handle_lock.acquire()
#			print("%s: lock acquired" % tag)

    def _release_lock(self, tag):
		if not _pyndn.is_run_executing(self.ndn_data):
#			print("%s: releasing lock" % tag)
            self._handle_lock.release()
#			print("%s: lock released" % tag)

    def fileno(self):
		return _pyndn.get_connection_fd(self.ndn_data)

    def process_scheduled(self):
		assert not _pyndn.is_run_executing(self.ndn_data), "Command should be called when ndn_run is not running"
		return _pyndn.process_scheduled_operations(self.ndn_data)

    def output_is_pending(self):
		assert not _pyndn.is_run_executing(self.ndn_data), "Command should be called when ndn_run is not running"
		return _pyndn.output_is_pending(self.ndn_data)

    def run(self, timeoutms):
		assert not _pyndn.is_run_executing(self.ndn_data), "Command should be called when ndn_run is not running"
        self._handle_lock.acquire()
        try:
			_pyndn.run(self.ndn_data, timeoutms)
        finally:
            self._handle_lock.release()

    def setRunTimeout(self, timeoutms):
		_pyndn.set_run_timeout(self.ndn_data, timeoutms)

    # Application-focused methods
    #
    def _expressInterest(self, name, closure, template = None):
        self._acquire_lock("expressInterest")
        try:
			return _pyndn.express_interest(self, name, closure, template)
        finally:
            self._release_lock("expressInterest")

    def expressInterest (self, name, onData, onTimeout = None, template = None):
        if not isinstance (name, Name):
            name = Name (name)
        self._expressInterest (name, 
                               Closure.TrivialExpressClosure (onData, onTimeout), 
                               template)

    def expressInterestForLatest (self, name, onData, onTimeout = None, timeoutms = 1.0):
        if not isinstance (name, Name):
            name = Name (name)
        self.expressInterest (name,
                              Closure.VersionResolverClosure (self, onData, onTimeout), 
                              Interest.Interest (interestLifetime = timeoutms, 
                                                 childSelector = Interest.CHILD_SELECTOR_LEFT))

    def _setInterestFilter(self, name, closure, flags = None):
        self._acquire_lock("setInterestFilter")
        try:
            if flags is None:
				return _pyndn.set_interest_filter(self.ndn_data, name.ndn_data, closure)
            else:
				return _pyndn.set_interest_filter(self.ndn_data, name.ndn_data, closure, flags)
        finally:
            self._release_lock("setInterestFilter")

    def setInterestFilter (self, name, onInterest, flags = None):
        if not isinstance (name, Name):
            name = Name (name)

        self._setInterestFilter (name, 
                                 Closure.TrivialFilterClosure (name, onInterest), 
                                 flags)

    def clearInterestFilter(self, name):
        if not isinstance (name, Name):
            name = Name (name)

        self._acquire_lock("setInterestFilter")
        try:
                        return _pyndn.clear_interest_filter(self.ndn_data, name.ndn_data)
        finally:
            self._release_lock("setInterestFilter")

    # Blocking!
    def get (self, name, template = None, timeoutms = 3000):
#		if not _pyndn.is_upcall_executing(self.ndn_data):
#			raise Exception, "Get called outside of upcall"

        if not isinstance (name, Name):
            name = Name (name)
        self._acquire_lock("get")
        try:
			return _pyndn.get(self, name, template, timeoutms)
        finally:
            self._release_lock("get")

    def put(self, contentObject):
        self._acquire_lock("put")
        try:
			return _pyndn.put(self, contentObject)
        finally:
            self._release_lock("put")


