from setuptools import find_packages, setup

setup(
    name='usta',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/emre/usta',
    license='MIT',
    author='Emre Yilmaz',
    author_email='mail@emreyilmaz.me',
    description='Personal file server',
    install_requires=['requests', 'flask', 'clint', 'gevent'],
    entry_points=dict(
        console_scripts=[
            'usta = usta.server:main',
            'usta_client = usta.client:main'
        ],
    ),
    classifiers=(
        'Programming Language :: Python :: 2.7',
    ),
)