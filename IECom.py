'''
----------------------------------------------------------------------------
"THE BEER-WARE LICENSE" (Revision 42):
<debasishm89_at_gmail.com> wrote this file.  As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return.   Debasish Mandal
----------------------------------------------------------------------------

Last Updated : 16.5.2014


'''

import thread
import os
from time import sleep
import logging
try:
	import win32com.client, pythoncom
except ImportError:
	print '[+] Could not import Win32Com Lib. Download and install from http://sourceforge.net/projects/pywin32/'
import time
from Helpers import Helpers
import sys
from datetime import datetime

class IECom:
	def __init__(self,PageHeap=False):
		print( '[+] '+ datetime.now().strftime("%Y:%m:%d::%H:%M:%S") +' Using Win32Com for fuzzing')
		self.ph = PageHeap
		self.help = Helpers()
		self.iePiD_p = None
		self.iePid_c = None
		self.StartUpPage = 'file://'+os.getcwd().replace('\\','/')+'\\Start.html'.replace('\\','/')
	def startfuzzer(self):
		print '[+] '+ datetime.now().strftime("%Y:%m:%d::%H:%M:%S") +' Killig all ie process if any exist system wide..'
		os.popen('taskkill /PID iexplore.exe /f')
		self.help.c = 1
		start_time = time.time()
		print '[+] '+ datetime.now().strftime("%Y:%m:%d::%H:%M:%S") +' Starting Fuzzer..'
		thread.start_new_thread(self.help.detectHungTab,())
		while 1:
			#print self.help.c
			#if self.help.CrashFlag:
			#	sleep(2)	# If there is any crash, let access violation handler finish its jobs ....
			if len(self.help.checkierunning()) == 2:
				#logging.info('[+] IE Running....Loading Tetscase....')
				try:
					url = self.help.generateTestCaseFile(insertAtan2=False)
				except Exception, e:
					print('[+] '+ datetime.now().strftime("%Y:%m:%d::%H:%M:%S") +' Error while generating test case file'+str(e))
					print e
					continue
				try:
					ie.Navigate(url+'?c='+str(self.help.c))
					if ie.Busy:
						sleep(0.5)
					self.help.c = self.help.c + 1	# +1 count only if Navigation successful
				except Exception, e:
					#print e
					continue
			else:
				print('[+] '+ datetime.now().strftime("%Y:%m:%d::%H:%M:%S") +' IE is not running launching ie prcess')
				try:
					sleep(2)										# Let it fully die.
					ie=win32com.client.Dispatch('internetexplorer.application')
					ie.Visible=1									# Set visibility to 1
					if self.help.StartMonitoringIE(PageHeap=self.ph):	# Attach to debugger. If True is retured everything is fine.
						sleep(1)									# It sometimes take time to generate the testcase path from attach loop					
						ie.Navigate(self.StartUpPage)				# Load start page
						help.CrashFlag = False
					else:
						# May be IE is not launched properly, More of less than 2 instance of IE process has been found in the system. So it better to killing the process.
						print ('[+] '+ datetime.now().strftime("%Y:%m:%d::%H:%M:%S") +' More of less than 2 instances of IE process has been found in the system.Kill all of them')
						self.help.killie()
				except Exception, e:
					print('[+] '+ datetime.now().strftime("%Y:%m:%d::%H:%M:%S") +' Could not launch new IE instance ..Will Try again..'+str(e))