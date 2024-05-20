from setuptools import setup, find_packages

setup(
    name='nsegpt',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    include_package_data=True,
    description='A package to fetch stock data from NSE India',
    author='NiftyBilla',
    author_email='kaushal.developer@yahoo.com',
    url='https://github.com/yourusername/nsefetcher',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
