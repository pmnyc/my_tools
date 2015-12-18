# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

This program is for renaming files or files in the folder
"""

import os

def rename(filename, new_filename):
    try:
        os.rename(filename, new_filename)
    except:
        pass
"""
# Below is a one-time process for some old files with old naming
    convention in Worcester,MA. I renamed them in the new stardard. 

### Batch Process the file names with new naming convention
for filename in os.listdir("."):
    if ('_' not in filename) and len(filename) == 24+len(".json"):
        filename_ = filename.replace(".json","")
        rename(filename, "worcester_ma_"+filename_[:12]+".json")
    else:
        continue
"""