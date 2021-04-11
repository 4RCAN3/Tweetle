from setuptools import setup, find_packages
from setuptools import *
from os import path


with open ("requirements.txt") as f:
    requirements = f.readlines()

long_description = r'''
<h1 align="center">Tweetle</h1>
<p align="center">
  <img src="https://user-images.githubusercontent.com/69053040/114283099-b0971d80-9a65-11eb-86b9-828b91979a82.png" alt = "Tweetle"/>
</p>
<p align="center"><i>A python based CLI to control your twitter account and get analytical data</i></p>
<p align="center">
  <a href="https://github.com/4RCAN3/Tweetle/stargazers"><img src="https://img.shields.io/github/stars/4RCAN3/Tweetle" alt="Stars Badge"/></a>
<a href="https://github.com/4RCAN3/Tweetle/network/members"><img src="https://img.shields.io/github/forks/4RCAN3/Tweetle" alt="Forks Badge"/></a>
<a href="https://github.com/4RCAN3/Tweetle/pulls"><img src="https://img.shields.io/github/issues-pr/4RCAN3/Tweetle" alt="Pull Requests Badge"/></a>
<a href="https://github.com/4RCAN3/Tweetle/issues"><img src="https://img.shields.io/github/issues/4RCAN3/Tweetle" alt="Issues Badge"/></a>
<a href="https://github.com/4RCAN3/Tweetle/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/4RCAN3/Tweetle?color=2b9348"></a>
<a href="https://github.com/4RCAN3/Tweetle/blob/master/LICENSE"><img src="https://img.shields.io/github/license/4RCAN3/Tweetle?color=2b9348" alt="License Badge"/></a>
</p>
<br>

<p align="center"><img src="https://media.discordapp.net/attachments/791081474425749577/830174345657450516/ezgif-7-0ab7a69f2594.gif" alt="Tweetle Gif"></p>


## Installation

### Through pip
#### For windows:
- `pip install tweetle`

#### For linux/macos:
- `pip3 install tweetle`
<br>

### Manual Installation
- `git clone https://github.com/4RCAN3/Tweetle/`
- `setup.bat`
- `venv\scripts\activate`
- `tweetle`


## Commands:
<p align="center"><img src="https://user-images.githubusercontent.com/69053040/114283653-70856a00-9a68-11eb-8737-137efbcd3a3e.png" alt = "commands">
</p>

<br>



## Languages used
<p align="center">
<img src = "https://img.shields.io/badge/python%20-%236C0101.svg?style=for-the-badge&logo=python&logoColor=white" alt="python"/> <img alt="MySQL" src="https://img.shields.io/badge/mysql-%2300f.svg?&style=for-the-badge&logo=mysql&logoColor=white"/>
</p>

## Contribute
Any contributions you make are **greatly appreciated**.

- PRs are accepted!!
- If you have some ideas for new features and you don't have time to implement them please open an issue with the tag new_feature.
- Please don't forget to comment (document) your code!


<p align="center"> <a href="https://ko-fi.com/N4N144R2L"><img src="https://ko-fi.com/img/githubbutton_sm.svg"/></a></p>
'''

setup(
    name='tweetle',
    version='0.1.9',
    author = "ARC4N3",
    author_email = "arcaneisc00l@gmail.com",
    url = "https://github.com/4RCAN3/Tweetle",
    description = "A CLI made to control your twitter account and get analytical data",
    long_description_content_type = "text/markdown",
    long_description = long_description,
    license = "MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "tweetle=tweetle.cli:cli"
        ]
    },
    classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
)

'''
Tweetle
ARC4N3,2021
'''