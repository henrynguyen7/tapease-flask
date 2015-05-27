import sys, os, logging

sys.path.insert(0, '/var/www/tapease')
os.chdir("/var/www/tapease")
logging.basicConfig(stream=sys.stderr)

from app import app as application