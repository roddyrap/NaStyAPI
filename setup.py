from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='NaStyAPI',
    version='0.3.0',
    packages=['NaStyAPI'],
    url='',
    license='Apache License 2.0',
    author='Roddy Rappaport',
    author_email='Roddy.Rappaport@gmail.com',
    description='A Python wrapper for the NationStates API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=["requests ~= 2.25.0", "ratelimit ~= 2.2.1"],
)
