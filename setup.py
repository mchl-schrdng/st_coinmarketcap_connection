from setuptools import setup, find_packages

setup(
    name='coinmarketcap_connection',
    version='0.1.0',
    author='Michaël Scherding',
    author_email='michael.Scherding@gmail.com',
    description='A Streamlit connector for the CoinMarketCap API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.dev/mchl-schrdng/st_coinmarketcap_connection',
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
)