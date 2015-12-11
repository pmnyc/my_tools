# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

This is just a template for timing how long a program takes to run

"""

from datetime import datetime
import re

start=datetime.now()

"""
Your program to run
"""

length = str(datetime.now()-start)
try:
    milsec = re.findall('.\d+',length)[-1]
except:
    milsec = ""
second = length.replace(milsec,"")

print("It took %s to run the program." %second)
