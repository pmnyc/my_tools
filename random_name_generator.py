# -*- coding: utf-8 -*-
"""
Create a random ID Name of length 12
@author: pm
"""

import string, random

def id_generator(size=12, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

print id_generator(12)