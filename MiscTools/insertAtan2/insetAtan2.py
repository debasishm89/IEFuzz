'''

Math.atan2(0xbabe, "[*] Line : ");

bu jscript9!Js::Math::Atan2 "du poi(poi(esp+14)+c);"

'''

import sys
f = open(sys.argv[1],'r')
d = f.readlines()
f.close()
for i in range(0,len(d)):
	log = 'Math.atan2(0xbabe, "[*] Line : '+ str(i) +'");'
	logged =  d[i].replace('\n',log)
	print logged