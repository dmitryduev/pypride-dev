from setuptools import setup

setup(name='pypride',
      version='2.0.0a',
      platforms=['Linux', 'MacOS X'],
      packages=['pypride'],
      package_dir={'pypride': 'pypride'},
      install_requires=['astropy>=3.2.1',
                        'jplephem>=2.9',
                        'numba>=0.45.1',
                        'numpy>=1.13',
                        'paramiko>=2.6.0',
                        'pysofa2>=18.1.30.4'
                        'requests>=2.22.0',
                        'scikit-learn>=0.21.3',
                        'scipy>=1.3.1']
      )
