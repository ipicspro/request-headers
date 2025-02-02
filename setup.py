from setuptools import setup, find_packages


setup(name='request-headers',
    version='0.1',
    url='https://github.com/ipicspro/request-headers',
    license='MIT',
    author='IS',
    author_email='info@ecommaker.com',
    description='Request header generator',
    #packages=find_packages(exclude=['tests']),
    packages=['request_headers'],
    long_description=open('README.md').read(),
    zip_safe=False,
    setup_requires=['nose'],
    install_requires=['requests', 'python-decouple', 'beautifulsoup4', 'fake-useragent==1.5.1'],
    test_suite='nose.collector')

