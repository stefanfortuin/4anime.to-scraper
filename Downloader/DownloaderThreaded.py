import os
import requests
from urllib.request import urlretrieve
from random import randrange
import threading
import sys
from tqdm import tqdm
import math

class FileDownloader():
	def __init__(self, max_threads=10):
		self.sema = threading.Semaphore(value=max_threads)
		self.threads = list()
		self.headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

	def t_getfile(self, link, filename, session):
		""" 
		Threaded function that uses a semaphore 
		to not instantiate too many threads 
		"""

		self.sema.acquire()	

		filepath = os.path.join(os.getcwd() + '/Downloads/' + str(filename))
		os.makedirs(os.path.dirname(filepath), exist_ok=True)
		
		if not os.path.isfile(filepath):

			block_size = 1024

			if session == None:
					
					try:
						request = requests.get(link, headers=self.headers, timeout=30, stream=True)
					except requests.exceptions.RequestException as e:
						print(e)
						sys.exit(1)
							
					with open(filepath, 'wb') as f:
						for chunk in request.iter_content(chunk_size=block_size):
							f.write(chunk)
					f.close()
					
					
			else:
				down_file = session.get(link, stream=True)

				with open(filepath, 'wb') as f:
					for chunk in down_file.iter_content(chunk_size=block_size):
						if chunk:
							f.write(chunk)
			
			print("completed file {0}".format(filename), end='\n')

		self.sema.release()

	def get_file(self, link, filename, session=None):
		""" Downloads the file"""
		thread = threading.Thread(target=self.t_getfile, args=(link, filename, session))
		self.threads.append(thread)
		thread.start()

	

