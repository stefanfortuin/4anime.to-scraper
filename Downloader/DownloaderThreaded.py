import os, sys, threading
import requests

class FileDownloader():
	def __init__(self, max_threads=10):
		self.sema = threading.Semaphore(value=max_threads)
		self.threads = list()
		self.headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
		self.block_size = 1024

	def t_getfile(self, link, filename, session):
		""" 
		Threaded function that uses a semaphore 
		to not instantiate too many threads 
		"""

		self.sema.acquire()	

		filepath = os.path.join(os.getcwd() + '/Downloads/' + str(filename))
		os.makedirs(os.path.dirname(filepath), exist_ok=True)
		
		if not os.path.isfile(filepath):
			print(f"downloading: {filename}")
			if session == None:
				try:
					request = requests.get(link, headers=self.headers, timeout=30, stream=True)
					self.write_file(request, filepath, 'wb')
				except requests.exceptions.RequestException as e:
					print(e)		
			else:
				request = session.get(link, stream=True)
				self.write_file(request ,filepath, 'wb')
		else:
			current_bytes = os.stat(filepath).st_size
			total_bytes = int(requests.head(link).headers['content-length'])

			if current_bytes < total_bytes:
				print(f"resuming: {filename}")
				range_header = self.headers.copy()
				range_header['Range'] = f"bytes={current_bytes}-{total_bytes}"

				try:
					request = requests.get(link, headers=range_header, timeout=30, stream=True)
					self.write_file(request, filepath, 'ab')
				except requests.exceptions.RequestException as e:
					print(e)
			else:
				print(f"already done: {filename}")
		
		self.sema.release()
	
	def write_file(self, content, filepath, writemode):
		with open(filepath, writemode) as f:
			for chunk in content.iter_content(chunk_size=self.block_size):
				if chunk:
					f.write(chunk)

		print(f"completed file {filepath}", end='\n')
		f.close()
		

	def get_file(self, link, filename, session=None):
		""" Downloads the file"""
		thread = threading.Thread(target=self.t_getfile, args=(link, filename, session))
		self.threads.append(thread)
		thread.start()

	

