from setuptools import setup, find_packages

setup(
    name='conspec_automation',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'conspec-automation=automator.main:main',
        ],
    },
)
