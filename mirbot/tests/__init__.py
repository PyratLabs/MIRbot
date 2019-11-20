#!/usr/bin/env python3

# ----------------------------------------------------------------------------
# MIRbot Tests
# (Modular Information Retrieval bot)
# ----------------------------------------------------------------------------
# Written by Xan Manning
# ----------------------------------------------------------------------------
#
# Copyright (c) 2017 PyratLabs (https://pyrat.co)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ----------------------------------------------------------------------------

# Import system modules
import os
import sys
import time
import copy
import random

# Import nose tests
from nose.tools import *

# Import our config and MIRCore modules
from mirbot.defaults import config
from mirbot import MIRCore


# Check we are running a good version of Python 3
if sys.version_info < (3,4):
	print("Your Python version may be too old.")
	print("Please upgrade to Python 3.4.x or above.")
	exit(1)




# Test importing of modules.
def test_import_modules():
	print("Initialize our MIRCore object.")
	assert MIRCore(config) != False


# Catch a failed connect
def test_failed_connect():
	print("Test a failed connection to a server.")
	core = MIRCore(config)
	try:
		core.connect()
	except SystemExit as iSE:
		if iSE.code > 0:
			assert True
		else:
			assert False


# Test a successful connect
def test_success_connect():
	print("Test a successful connection to a server.")
	test_config = config
	test_config['nick'] = 'MIRTrv[%d]' % random.randint(0, 100)
	test_config['name'] = 'MIRTrv[%d]' % random.randint(0, 100)
	test_config['server'] = 'irc.freenode.org'
	test_config['channels'] = ['#pyrat']
	test_config['sqlite_db'] = 'Travis.db'
	test_config['logging'] = True
	test_config['logging_trim'] = True
	test_config['welcome_new'] = False
	test_config['say_online'] = False
	test_config['owner'] = 'MIRbot'
	test_config['commands'] = ["QUIT :Testing Complete"]

	test_core = MIRCore(test_config)
	try:
		test_core.connect()
		time.sleep(2)

		for connectCommand in test_config['commands']:
			test_core.send(connectCommand)

		test_core.listen()
	except SystemExit as iSE:
		if iSE.code > 0:
			assert False
		else:
			assert True


# Testing out some MIRCore functions.
def test_core_functions():
	print("Test some of our vital MIRCore functions.")
	test_config = config
	test_config['nick'] = 'MIRTrv[%d]' % random.randint(0, 100)
	test_config['name'] = 'MIRTrv[%d]' % random.randint(0, 100)
	test_config['server'] = 'irc.freenode.org'
	test_config['channels'] = ['#pyrat']
	test_config['sqlite_db'] = 'Travis.db'
	test_config['logging'] = True
	test_config['logging_trim'] = True
	test_config['welcome_new'] = False
	test_config['say_online'] = False
	test_config['owner'] = 'MIRbot'
	test_config['commands'] = [
		"NOTICE #pyrat :Testing Complete: Python %s.%s.%s."
			% sys.version_info[:3],
		"QUIT :Testing Complete."
	]

	test_core = MIRCore(test_config)

	test_core.connect()
	time.sleep(2)

	print("Rejoin channels")
	test_core.rejoin()
	if len(test_core.joined_channels) < 1:
		assert False

	time.sleep(2)

	print("Peform a MIRCore config clean.")
	test_core.clean()
	if len(test_core.joined_channels) > 0:
		assert False

	time.sleep(2)

	print("Check modules unloaded.")
	print(len(test_core.loaded_modules))
	if len(test_core.loaded_modules) > 0:
		assert False

	time.sleep(2)

	print("Perform a MIRCore config clean with module reload.")
	test_core.clean(True)

	print("Check modules reloaded.")
	print(len(test_core.loaded_modules))
	if len(test_core.loaded_modules) < 1:
		assert False

	time.sleep(2)

	print("Check method function: Found Method")
	if test_core.methodExistsInClass("u_help") == False:
		assert False

	time.sleep(2)

	print("Check method function: Missing Method")
	if test_core.methodExistsInClass("u_missing") == True:
		assert False

	time.sleep(2)

	print("Check method in module function: Found Method")
	if test_core.methodExists("u_afk") == False:
		assert False

	time.sleep(2)

	print("Check method in module function: Missing Method")
	if test_core.methodExists("u_missing_module") == True:
		assert False

	time.sleep(2)

	print("Call a test method")
	if test_core.callMethodInClass("u_pytest") == False:
		assert False

	time.sleep(2)

	print("Get Variable from SQLite database")
	test_salt = test_core.get_variable('salt')
	if test_salt == False or test_salt == None:
		assert False
	else:
		print(test_salt)

	time.sleep(2)

	print("Set Variable to SQLite database")
	test_var = test_core.set_variable('travis', test_core.unixtime())
	test_var_read = test_core.get_variable('travis', False)
	if test_var == False or test_var_read == False:
		assert False
	else:
		print(test_var_read)

	time.sleep(2)
	test_core.connect()

	for connectCommand in test_config['commands']:
		test_core.send(connectCommand)

	try:
		test_core.listen()
	except SystemExit as iSE:
		if iSE.code > 0:
			assert False
		else:
			assert True
