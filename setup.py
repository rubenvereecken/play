import os
from setuptools import setup, find_packages

setup(
    name='play',
    version="1.0.0",
    description='Tools for human play of games popular in Reinforcement Learning',
    author='Ruben Vereecken',
    url='',
    packages=find_packages(),
    # packages=['play'],
    install_requires=['gym', 'gym_vgdl', 'gym_recording'],
    entry_points={
        'console_scripts': [
            'play-vgdl = play.play_vgdl:main',
            'gymrat = play.gymrat:main',
            'list-gym-envs = play.list_envs:main',
        ]
    }
)

