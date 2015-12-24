'''
----------------------------------------------------------------------------
"THE BEER-WARE LICENSE" (Revision 42):
<debasishm89_at_gmail.com> wrote this file.  As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return.   Debasish Mandal
----------------------------------------------------------------------------

To run this fuzzer you have to make follwing changes in IE: 

1. Since this fuzzer loads the testcase locally (eg. D:\\testcase\\testcase.html) as file.
You must turn off the prompt for Internet Explorer by following 

Tools (menu) -> Internet Options -> Security (tab) -> Custom Level (button) -> Disable Automatic prompting for ActiveX controls.

2. You also need to disable IE protected mode to be able to control Internet Explorer using Python 'win32com'.

 -> Internet Options -> Security -> Trusted Sites    : Low
 -> Internet Options -> Security -> Internet         : Medium + unchecked Enable Protected Mode
 -> Internet Options -> Security -> Restricted Sites : unchecked Enable Protected Mode

Last Updated : 26.7.2014

'''
from IECom import IECom
import sys
from os import environ
import optparse

class IEFuzz():
	def __init__(self):
		None
	def PrintBanner(self):
		print '''
		 _____  ________   ________                        		
		|_   _||_   __  | |_   __  |                       		
		  | |    | |_ \_|   | |_ \_|__   _   ____   ____   		
		  | |    |  _| _    |  _|  [  | | | [_   ] [_   ]  		
		 _| |_  _| |__/ |  _| |_    | \_/ |, .' /_  .' /_  		
		|_____||________| |_____|   '.__.'_/[_____][_____] 		
                                           		        
		A static Internet Explorer Fuzzer		
		Author :DEBASISH MANDAL ( @debasishm89 )		
		'''
	def PrintHelp(self):
		print '\t\tUsage : '
		print '\t\t./IEFuzz.py => Run fuzzer normally ' 
		print '\t\t./IEFuzz.py PageHeap => Run fuzzer + Monitor PAGE_GUARD access violation. Use this while fuzzing with PageHeap enabled' 
if __name__ == "__main__":
	f = IEFuzz()
	# Check environment first.
	if 'PROGRAMFILES(X86)' in environ:
		print '[+] Currently 64bit OS is not supported(Pydbg only supports x86).Please run it on 32 bit Windows'
		exit()
	else:
		if len(sys.argv) == 2 and sys.argv[1] == "PageHeap":
			f.PrintBanner()
			com = IECom(PageHeap=True)
			com.startfuzzer()
		elif len(sys.argv) == 1:
			# No Page heap
			f.PrintBanner()
			com = IECom(PageHeap=False)
			com.startfuzzer()
		else:
			f.PrintBanner()
			f.PrintHelp()
			print '[+] Invalid Option'