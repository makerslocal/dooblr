from setuptools import setup

import dooblr

if __name__ == "__main__":

    with open('requirements.txt', 'r') as f:
        install_requires = [x for x in list(f) if x[0] != '-']

    with open('test-requirements.txt', 'r') as f:
        test_requires = [x for x in list(f) if x[0:2] != '-r']
    
    with open('README.rst', 'r') as infile:
        long_description = infile.read()
    
    setup(
        name='dooblr',
        description='Duplicate data received over MQTT to InfluxDB',
        long_description=long_description,
        author='Tyler Crumpton',
        author_email='tyler.crumpton@gmail.com',
        url='https://github.com/makerslocal/dooblr',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: ISC License (ISCL)',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
        ],
        license='ISC',
        setup_requires=['tcversioner'],
        install_requires=install_requires,
        tests_require=test_requires,
        tcversioner={
            'version_module_paths': ['dooblr/_version.py'],
            'use_dev_not_post': True
        },
        packages=['dooblr'],
        entry_points={
            'console_scripts': [
                'dooblr = dooblr.main:main'
            ]
        },
    )
