from setuptools import setup, find_packages

setup(
    name='cookbook',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'marshmallow',
        'PyYaml'
    ],
    extras_require={
        'dev': [
            'pytest'
        ]
    },
    entry_points='''
        [console_scripts]
        cookbook=cookbook.scripts.cli:cli
    ''',
)