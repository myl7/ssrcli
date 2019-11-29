import re
from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('ssrcli/__init__.py') as f:
    version = re.search(r'__version__ = \'(.*)\'', f.read()).group(1)

reqs = ['peewee', 'requests', 'xdg']

test_reqs = ['pytest', 'twisted', 'pytest-ordering', 'pytest-cov']

setup(
    name='ssrcli',
    author='myl',
    author_email='myl7@gmail.com',
    url='https://github.com/myl7/ssrcli',
    description='SSR client with shell interface and using Docker to deploy',
    keywords=['ssr', 'ssrcli'],
    long_description=readme,
    long_description_content_type='text/markdown',
    version=version,
    packages=['ssrcli'],
    license='MIT',
    python_requires='>=3.6',
    install_requires=reqs,
    tests_require=test_reqs,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX :: Linux',
        'Topic :: Internet :: Proxy Servers',
    ],
    entry_points={
        'console_scripts': [
            'ssrcli = ssrcli.cli:main',
        ],
    },
)
