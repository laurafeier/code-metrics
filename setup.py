from setuptools import setup, find_packages

setup(
    name='code-metrics',
    version='1.0.0',
    description='Code analysis tool',
    author='Laura Feier',
    author_email='feierlaura10@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'mando',
        'tabulate',
        'radon',
        'pylint',
        'jira',
        'requests',
        'gitpython',
    ],
    entry_points={
        'console_scripts': [
            'code_metrics = code_metrics.commands:main'
        ]
    },
)
