from setuptools import setup

setup(
    name='wikitransbot',
    version='1.0.0',
    author='Jef Roelandt',
    author_email='roelandt.jef@protonmail.com',
    url='https://github.com/SuperMeepBoy/wikitransbot',
    py_modules=['wikitransbot'],
    install_requires=['tweepy'],
    extras_requires={
        'test': ['pytest', 'flake8'],
    },
)
