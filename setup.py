import re
from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('ssrcli/__init__.py') as f:
    version = re.search(r'__version__ = \'(.*)\'', f.read()).group(1)

setup(
    name='ssrcli',
    author='myl7',
    author_email='myl7.ustc@gmail.com',
    url='https://github.com/myl7/ssrcli',
    description='SSR management client with shell interface',
    keywords=['ssr', 'ssr-client'],
    long_description=readme,
    long_description_content_type='text/markdown',
    version=version,
    packages=['ssrcli'],
    license='MIT',
    platforms=['Linux'],
    python_requires='>=3.6',
    install_requires=['peewee', 'requests', 'xdg'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: Proxy Servers',
        'Typing :: Typed',
    ],
    entry_points={
        'console_scripts': [
            'ssrcli = ssrcli.cli:main',
        ],
    },
    zip_safe=True,
)
