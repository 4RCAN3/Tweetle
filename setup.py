from setuptools import setup, find_packages


def read_requirements():
    with open('requirements.txt') as req:
        content = req.read()
        requirements = content.split('\n')

setup(
    name = 'tweetle',
    version = '0.1',
    packages = find_packages(),
    include_package_data = True,
    install_requires = read_requirements(),
    entry_points = '''
    [console_scripts]
    tweetle = tweetle.cli:cli
    '''
)