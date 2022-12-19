import logging
import os
import threading
import time
import random
import string
import subprocess
import requests


import socket
import faulthandler
faulthandler.enable()

socket.setdefaulttimeout(600)

botStartTime = time.time()
if os.path.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

SERVER_PORT = os.environ.get('SERVER_PORT', None)
PORT = os.environ.get('PORT', SERVER_PORT)
web = subprocess.Popen([f"gunicorn wserver:start_server --bind 0.0.0.0:{PORT} --worker-class aiohttp.GunicornWebWorker"], shell=True)
time.sleep(1)
