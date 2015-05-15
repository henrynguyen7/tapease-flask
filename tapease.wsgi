import sys, os
sys.path.insert(0, '/var/www/tapease')
os.chdir("/var/www/tapease")

from app import app as application
