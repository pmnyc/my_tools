"""
@author: Man Peng
"""

__all__ = ['__version__', 'version_info']

# Crawler version
__version__ = ""
# import pkgutil
# __version__ = pkgutil.get_data(__package__, 'VERSION').decode('ascii').strip()
# version_info = tuple(int(v) if v.isdigit() else v
#                     for v in __version__.split('.'))
# del pkgutil

# Check minimum required Python version, it needs to be >= 2.7
import sys
if sys.version_info < (2, 7):
    print("This software version %s requires Python 2.7" % __version__)
    sys.exit(1)

# Ignore noisy twisted deprecation warnings
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning, module='twisted')
del warnings

# Load Basic Packages
import scrapy
