from setuptools import setup, find_packages

setup(
    name='SSH-IDS',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'aiohttp==3.9.5',
        'aiohttp-retry==2.8.3',
        'aiosignal==1.3.1',
        'attrs==23.2.0',
        'certifi==2024.2.2',
        'charset-normalizer==3.3.2',
        'colorama==0.4.6',
        'configparser==7.0.0',
        'frozenlist==1.4.1',
        'idna==3.7',
        'IP2Location==8.10.2',
        'multidict==6.0.5',
        'PyJWT==2.8.0',
        'pytz==2024.1',
        'requests==2.31.0',
        'setuptools==69.5.1',
        'urllib3==2.2.1',
        'yarl==1.9.4',
    ],
    entry_points={
        'console_scripts': [
            'ssh_alert=console:start_interactive_console',
        ],
    },
    author='Prabhakar',
    author_email='prabhakarpal666@gmail.com',
    description='A script to alert admin of failed SSH attempts and block IPs',
    url='https://github.com/git-prabhakar/SSH-IDS',
)
