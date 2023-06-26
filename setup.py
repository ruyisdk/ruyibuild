import os
import setuptools
import re


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(SCRIPT_DIR)

print (SCRIPT_DIR)

with open('README.md', 'r') as f:
    long_description = f.read()

with open('src/constant.py', 'r') as f:
    lines=f.readlines()
    for line in lines:
        if 'version =' in line:
            version = re.search("(version = ')(.*)(')", line).group(2)


setuptools.setup(
    name='ruyibuild',
    version=version,
    author='Jean',
    author_email='',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitee.com/geasscore/ruyibuild/tree/develop/',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    install_requires=[
        'setuptools',
        'docker',
        'GitPython',
        'ruamel.yaml'
    ],
    python_requires='>=3.8',
    entry_points={'console_scripts': ('ruyibuild = src.main:main',)},
)