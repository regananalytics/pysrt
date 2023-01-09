from setuptools import setup

with open('requirements.txt') as f:
    required = f.readlines()

setup(
    name='pysrt',
    version='0.0.1',
    packages=['pysrt'],
    url='',
    license='',
    author='Dan Regan (SoundOfWaffles)',
    author_email='dan@regan-analytics.com',
    description='A Speedrunning Tool written in Python',
    install_requires=required,
    python_requires='>=3.10'
)
