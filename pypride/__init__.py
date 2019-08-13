import os
import requests


def fetch_cats(_cache_dir):
    cats_dir = os.path.join(_cache_dir, 'cats')
    if not os.path.exists(cats_dir):
        os.makedirs(cats_dir)

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
                with open(os.path.join(cats_dir, cat), 'wb') as f:
                    f.write(r.content)
                    print(f'Fetched {url}')
            else:
                print(f'Failed to fetch {url}')

        except Exception as e:
            print(f'Failed to fetch {url}: {str(e)}')


__version__ = '2.0.0'


homedir = os.environ['HOME']

cache_dir = os.path.join(homedir, '.pypride')

if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

    # fetch catalogs on first run
    fetch_cats(cache_dir)
