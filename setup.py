from setuptools import find_packages, setup

setup(
    name='bridge_env',
    version='0.1.0',
    description='Contract bridge environment.',
    author='yotaroy',
    url='https://github.com/yotaroy/bridge_env',
    author_email='yyamaguchi643@gmail.com',
    license='MIT',
    install_requires=['numpy'],
    extras_require={
        'dev': ['flake8', 'mypy', 'pytest', 'pytest-mock'],
    },
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'bridge-server = bridge_env.network_bridge.server:main',
            'bridge-client-ex = bridge_env.network_bridge.client:main'
        ]
    }
)
