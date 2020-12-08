from setuptools import setup, find_packages

setup(
    name = 'ck_direct_upload',
    version='0.0.1',
    description = 'Directly move large files as ressources into Ckan',
    url = 'https://github.com/eawag-rdm/ck_direct_upload',
    author='Harald von Waldow',
    author_email='harald.vonwaldow@eawag.ch',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3.0',
        'Programming Language :: Python :: 3',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.5, <4',
    # install_requires=['peppercorn'],
    # entry_points={  
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
)
