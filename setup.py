from setuptools import setup, find_packages

setup(
    name='cookbook',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'boto3',  # I'd love ot have this only be imported if planning to run with dynamo backend
        'Click',
        'marshmallow',
        'PyYaml'
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-terraform',
            'pytest-docker'
        ]
    },
    entry_points='''
        [console_scripts]
        cookbook=cookbook.scripts.cli:cli
    ''',
)
