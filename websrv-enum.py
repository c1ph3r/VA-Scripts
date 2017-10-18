#!/usr/bin/env python
#
# Find web server running in an ip ranges(CIDR) and capturing webpage as an image(png).
#----------------------------------------------------------------------------------------------#
# websrv-enum.py v0.1                                                                          #
# (C)opyright 2011 - Krit Kadnok <c1ph3r[at]blackbuntu.com>                                    #
#---License------------------------------------------------------------------------------------#
#  This program is free software: you can redistribute it and/or modify it under the terms     #
#  of the GNU General Public License as published by the Free Software Foundation, either      #
#  version 3 of the License, or (at your option) any later version.                            #
#                                                                                              #
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;   #
#  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.   #
#  See the GNU General Public License for more details.                                        #
#                                                                                              #
#  You should have received a copy of the GNU General Public License along with this program.  #
#  If not, see <http://www.gnu.org/licenses/>.                                                 #
#---Important----------------------------------------------------------------------------------#
#                     *** Do NOT use this for illegal or malicious use ***                     #
#              The programs are provided as is without any guarantees or warranty.             #
#----------------------------------------------------------------------------------------------#
import re
import os
import sys
import time
import requests
import threading
from netaddr import *

class colors:
     BLUE='\033[94m'
     GREEN='\033[92m'
     YELLOW='\033[93m'
     RED='\033[91m'
     ENDC='\033[0m'
		
def getWebServer(ip, ports, msg):
	for port in ports:
		try:
			with requests.session() as s:
				headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"}
				req = s.get("http://"+ip+":"+str(port), headers=headers)
				server = req.headers['Server']
				if server:
					print("[+] IP:"+ip,"Port:"+str(port),"Running:",server)
					os.system('CutyCapt --url=http://%s:%s --out=%s%s_%s.png'%(ip,str(port),thumbs_dir,ip,str(port)))
				else:
					print("Unable to find Web Server on "+ip)
		except: pass

#########################################################################
if __name__ == "__main__":

# Banner
	print colors.GREEN+'''
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
||                                                                        ||
||    Web Server Enumeration Tool                                         ||
||    Written by Krit Kadnok < c1ph3r@blackbuntu.com >                    ||
||    Visit: www.blackbuntu.com                                           ||
||                                                                        ||
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
'''+colors.ENDC

	# Define ports
	ports = [80,8000,8080,10000]
	# Help
	if len(sys.argv) != 2:
		print colors.RED+"Usage:   "+colors.ENDC,colors.BLUE+"python",sys.argv[0],"<network>"+colors.ENDC
		print colors.BLUE+"          You can specify IP address value and the CIDR prefix like this:"+colors.ENDC
		print colors.RED+"Example: "+colors.ENDC,colors.BLUE+"python",sys.argv[0],"192.168.0.0/24"+colors.ENDC
		print colors.RED+"Example: "+colors.ENDC,colors.BLUE+"python",sys.argv[0],"192.168.0.0/21"+colors.ENDC
		sys.exit(1)

	# Get current working directory
	current_dir = os.getcwd()
	# If directory thumbs doesn't exist, create thumbs dir.
	if not os.path.exists(current_dir+'/thumbs'):
		try:
			os.mkdir('thumbs')
		except: pass

	thumbs_dir = current_dir+'/thumbs/'

	try:
		network = sys.argv[1]
	except(ValueError):
		print colors.RED+"[-] Incorrect Network values\n"+colors.ENDC
		sys.exit(1)

	total_ip = IPNetwork(network)
	print colors.RED+"\n[+] Scanning:"+colors.ENDC,len(total_ip)-2,"ips\n"
	print "save capture image to "+thumbs_dir

	for ip in IPNetwork(network).iter_hosts():
		ip = str(ip).strip()
		time.sleep(1)
		threading.Thread( target=getWebServer, args=(ip, ports, 0) ).start()
