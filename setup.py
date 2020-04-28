from setuptools import setup, find_packages

#with open('README.md') as f:
#    readme = f.read()

#with open('LICENSE') as f:
#    license = f.read()

with open('requirements.txt') as f:
    reqs = f.read()

setup(
    name='web-crawler',
    version='0.1',
    description='crawing web data using given strategies',
    #long_description=readme,
    #license=license,
    python_requires='>=3.6',
    packages=find_packages(exclude=('data')),
    #install_requires=reqs.strip().split('\n'),
)