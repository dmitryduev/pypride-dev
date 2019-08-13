from setuptools import setup

setup(name='pypride',
      version='2.0.0',
      platforms=['Linux', 'MacOS X'],
      packages=['pypride'],
      package_dir={'pypride': 'pypride'},
      install_requires=['astropy>=3.2.1',
                        'jplephem>=2.9',
                        'numpy>=1.13',
                        'requests>=2.22.0']
      )
