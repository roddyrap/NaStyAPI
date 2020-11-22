from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='NS-Api',
    version='0.1',
    packages=['NSapi'],
    url='',
    license='CC Attribution 4.0 International',
    author='Roddy Rappaport',
    author_email='Roddy.Rappaport@gmail.com',
    description='A Python wrapper for the NationStates API',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
