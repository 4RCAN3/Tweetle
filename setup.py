from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as req:
        content = req.read()
        requirements = content.split('\n')

def long_description():
    with open("README.md", encoding = "utf-8") as f:
        long_description = f.read()
    return long_description

setup(
    name='tweetle',
    version='0.1.0',
    author = "ARC4N3",
    author_email = "arcaneisc00l@gmail.com",
    url = "https://github.com/4RCAN3/Tweetle",
    description = "A CLI made to control your twitter account and get analytical data",
    long_description = long_description(),
    long_description_content_type = "text/markdown",
    license = "MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points='''
    [console_scripts]
    tweetle=tweetle.cli:cli
    ''',
)

'''
Tweetle
ARC4N3,2021
'''