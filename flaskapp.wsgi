#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,”/Users/andershellstrom/git/resurseffektivitet/“)

from app import app as application
application.secret_key = "jhkhkjhkjhkjhkjhkjhk"

