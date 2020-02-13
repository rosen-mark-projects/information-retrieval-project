from setuptools import setup, find_packages


with open('requirements.txt') as fp:
    requirements = fp.read()

setup(
    name="twitter-IR",
    version="0.1",
    packages=find_packages(),
    nstall_requires=requirements,
    extras_require={
        'dev': ['ipython', 'ipdb'],
    },
)
