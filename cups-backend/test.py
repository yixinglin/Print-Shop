import time

from core.db import *

while (True):
    backup_database()
    time.sleep(1) # Run every hour