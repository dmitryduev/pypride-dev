import os
import requests


def get_cats():
    """
        Get necessary catalogs and ephemerides from Github repo
    :return:
    """
    try:
        _homedir = os.environ['HOME']
        _cache_dir = os.path.join(_homedir, '.pypride')

        # should be unnecessary
        if not os.path.exists(_cache_dir):
            os.makedirs(_cache_dir)

        # fetch catalogs
        fetch_cats(_cache_dir)

        # fetch eph
        fetch_eph(_cache_dir)

    except Exception as e:
        print(f'Failed to update catalogs and ephemerides: {str(e)}')


def fetch_cats(_cache_dir):
    _cats_dir = os.path.join(_cache_dir, 'cats')
    if not os.path.exists(_cats_dir):
        os.makedirs(_cats_dir)

    # base_url = 'https://raw.githubusercontent.com/dmitryduev/pypride/master/pypride/cats/'
    base_url = 'https://raw.githubusercontent.com/dmitryduev/pypride-dev/master/pypride/cats/'

    cats = ['ant.shn',
            'antenna-info.txt',
            'eopc04.cat',
            'glo.sit',
            'glo.src',
            'glo.vel',
            'got.blq',
            'ns-codes.txt',
            'ramp.mex',
            'ramp.vex',
            'ramp1w.mex',
            'ramp1w.vex',
            'rfc_2011a.axof',
            'rfc_2014b_cat.txt',
            'sc.freq',
            'sched.cat',
            'source.names',
            'station.names',
            'tpxo72.blq']

    for cat in cats:
        try:
            url = os.path.join(base_url, cat)

            r = requests.get(url)

            if r.status_code == 200:
                with open(os.path.join(_cats_dir, cat), 'wb') as f:
                    f.write(r.content)
                    print(f'Fetched {url}')
            else:
                print(f'Failed to fetch {url}')

        except Exception as e:
            print(f'Failed to fetch {url}: {str(e)}')


def fetch_eph(_cache_dir):
    _eph_dir = os.path.join(_cache_dir, 'jpl_eph')
    if not os.path.exists(_eph_dir):
        os.makedirs(_eph_dir)

    # base_url = 'https://raw.githubusercontent.com/dmitryduev/pypride/master/pypride/jpl_eph/'
    base_url = 'https://raw.githubusercontent.com/dmitryduev/pypride-dev/master/pypride/jpl_eph/'

    ephs = ['de403.bsp', 'de405.bsp', 'de421.bsp', 'de430.bsp']

    for eph in ephs:
        try:
            url = os.path.join(base_url, eph)

            r = requests.get(url)

            if r.status_code == 200:
                with open(os.path.join(_eph_dir, eph), 'wb') as f:
                    f.write(r.content)
                    print(f'Fetched {url}')
            else:
                print(f'Failed to fetch {url}')

        except Exception as e:
            print(f'Failed to fetch {url}: {str(e)}')


__version__ = '2.0.0'


homedir = os.environ['HOME']

cache_dir = os.path.join(homedir, '.pypride')
cats_dir = os.path.join(cache_dir, 'cats')
eph_dir = os.path.join(cache_dir, 'jpl_eph')


if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

    # fetch catalogs on first run
    fetch_cats(cache_dir)

    # fetch DE430 on first run
    fetch_eph(cache_dir)

    # make aux dirs:
    if not os.path.exists(os.path.join(cache_dir, 'ion')):
        os.makedirs(os.path.join(cache_dir, 'ion'))
    if not os.path.exists(os.path.join(cache_dir, 'meteo')):
        os.makedirs(os.path.join(cache_dir, 'meteo'))
    if not os.path.exists(os.path.join(cache_dir, 'sc_eph')):
        os.makedirs(os.path.join(cache_dir, 'sc_eph'))
    for sc_name in ('mex', 'vex', 'rosetta', 'radioastron', 'gnss', 'gaia', 'mro'):
        pth = os.path.join(cache_dir, 'sc_eph', 'raw_' + sc_name)
        if not os.path.exists(pth):
            os.makedirs(pth)

# import all class declarations
from .classes import *
