import os

__version__ = '2.0.0'


homedir = os.environ['HOME']

cache_dir = os.path.join(homedir, '.pypride')

if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

# fetch catalogs