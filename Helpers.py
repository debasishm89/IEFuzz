'''
----------------------------------------------------------------------------
"THE BEER-WARE LICENSE" (Revision 42):
<debasishm89_at_gmail.com> wrote this file.  As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return.   Debasish Mandal
----------------------------------------------------------------------------

Last Updated : 16.5.2014

'''
import sys
from pydbg import *
from pydbg.defines import *
from time import sleep
import os
import gc
import utils
import shutil
from datetime import datetime
#from TestCase import TestCase
import thread
import logging
from glob import glob
import imp
from random import choice
class Helpers:
	def __init__(self):
		self.c = 1
		self.TestCasePath = None
		self.CrashFlag = False
		self.pids = []
		self.all_test_cases = []
		self.LoadTestCases()
	def av_handler(self,dbg):
		'''
		Handle access violation / guard page access vilation.
		'''
		self.CrashFlag = True
		programname = "C:\\Program Files\\Internet Explorer\\iexplore.exe"
		print '[+] '+  datetime.now().strftime("%Y:%m:%d::%H:%M:%S") +' BOOM!! IE Crashed'
		crash_bin = utils.crash_binning.crash_binning()
		crash_bin.record_crash(dbg)
		violation_addr = hex(dbg.dbg.u.Exception.ExceptionRecord.ExceptionInformation[1])
		thetime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
		crashfilename = 'crash_'+programname.split('\\',programname.count('\\'))[-1]+'_'+'_'+ thetime +'.html'
		synfilename = 'crashes\\'+ violation_addr +'\\crash_'+programname.split('\\',programname.count('\\'))[-1]+'_'+'_'+ thetime +'.txt'
		if not os.path.exists('crashes\\'+violation_addr):
			os.makedirs('crashes\\'+violation_addr)
		shutil.copyfile(self.TestCasePath,'crashes\\'+violation_addr+'\\'+crashfilename)
		print ('[+] '+ datetime.now().strftime("%Y:%m:%d::%H:%M:%S") +' Crash file Copied to '+violation_addr+'\\'+crashfilename)
		syn = open(synfilename,'w')
		syn.write(crash_bin.last_crash_synopsis())
		syn.close()
		print '[+] '+ datetime.now().strftime("%Y:%m:%d::%H:%M:%S")+' Killing half dead process'
		self.killie()
		return DBG_CONTINUE
	def checkierunning(self):
		'''
		Parse process list and return a list with all iexplore.exe PIDs.
		'''
		ie_pids = []
		dbg1 = pydbg()
		for (pid,name) in dbg1.enumerate_processes():
			if name == 'iexplore.exe':
				ie_pids.append(pid)
		del dbg1
		return ie_pids
	def killie(self):
		print ('[+] '+ datetime.now().strftime("%Y:%m:%d::%H:%M:%S") +' Killing IE ')
		os.popen('taskkill /PID iexplore.exe /f')
		gc.collect()
		self.pids = []
		print ('[+] '+ datetime.now().strftime("%Y:%m:%d::%H:%M:%S") +' Killing IE done..')
	def attach_debugger(self,pid,PageHeap):
		# Attach debugger to Parent IE Process Broker
		try:
			print ('[+] '+ datetime.now().strftime("%Y:%m:%d::%H:%M:%S") +' Attaching IE process to Debugeer :'+str(pid))
			dbg_p = pydbg()
			dbg_p.attach(pid)
			dbg_p.set_callback(EXCEPTION_ACCESS_VIOLATION, self.av_handler)	# Normal Read/Write AV
			if PageHeap:
				print ('[+] '+ datetime.now().strftime("%Y:%m:%d::%H:%M:%S")+' GUARD_PAGE Access will be monitored')
				dbg_p.set_callback(EXCEPTION_GUARD_PAGE, self.av_handler)		# Required while page heap is enabled
			dbg_p.run()
		except Exception, e:
			print ('[+] '+ datetime.now().strftime("%Y:%m:%d::%H:%M:%S") +' Could not attach to process..'+str(pid)+str(e))	
			self.killie()
	def detectHungTab(self):
		'''
		Typical IE feature :P, it will be surely be stuck, every now and then. :\ :/
		This will run as a thread and check when IE is stuck. If IE is stuck it will kill it completely, and main thread will relauch it.	
		'''
		print ('[+] '+ datetime.now().strftime("%Y:%m:%d::%H:%M:%S") +' Hang Detector Started')
		status = self.c
		while 1:
			sleep(10)
			if status == self.c:
				print ('[+] '+ datetime.now().strftime("%Y:%m:%d::%H:%M:%S") +' Tab is not responding..')
				if self.CrashFlag:	# Just for handling badluck..In the meantime if IE crashes, delay the murder for 2 seconds.
					sleep(2)
				self.killie()
			else:
				status = self.c
	def LoadTestCases(self):
		'''
		Load test cases from /TestCases folder.
		
		'''
		mods = glob("TestCases/*.py")
		for path in mods:
			print '[+] '+datetime.now().strftime("%Y:%m:%d::%H:%M:%S")+' Loading Test Cases : ',path
			foo = imp.load_source('TestCase',path)
			#tc = foo.TestCase(insertAtan2=False)
			self.all_test_cases.append(foo)
	def generateTestCaseFile(self,insertAtan2=False):
		fo = open(self.TestCasePath,'w')
		# When more than one test case is provided, Randomly choose any test case and generate a test case.
		fo.write(choice(self.all_test_cases).TestCase(insertAtan2=False).getFinalTestCase())  # Writing the html + JS test case in the temp file.
		fo.close()
		return 'file://'+self.TestCasePath.replace('\\','/')
	def StartMonitoringIE(self,PageHeap):
		'''
		attach IE to debugger.
		'''
		self.pids = self.checkierunning()
		print ('[+] '+ datetime.now().strftime("%Y:%m:%d::%H:%M:%S") +' IE PIDS => '+ str(self.pids))
		if len(self.pids) == 2:
			self.TestCasePath = os.getcwd()+'\\temp\\'+str(self.pids[0])+'-'+str(self.pids[1])+'.html'
			for pid in self.pids:
				thread.start_new_thread(self.attach_debugger,(pid,PageHeap,))
				sleep(0.5)
			return True
		else:
			return False