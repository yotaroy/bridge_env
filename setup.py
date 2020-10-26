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
    packages=find_packages(exclude=('script', 'tests'))
)
