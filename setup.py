from setuptools import setup, find_packages

setup(name='soldat-pymapper',
      version='0.1.0',
      packages=find_packages(),
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'pymapper = ui:main',
              'mapacker = utils.mapacker:main',
          ]
      }
      )
