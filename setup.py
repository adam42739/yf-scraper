from setuptools import setup

setup(
    name="yfscraper",
    version="0.2.0",
    description="Tool for scraping stock data from yahoo.com",
    url="https://github.com/adam42739/yf-scraper",
    author="Adam Lynch",
    author_email="aclynch@umich.edu",
    license="MIT License",
    packages=["yfscraper", "yfscraper.v1", "yfscraper.v2"],
    install_requires=[
        "pandas>=2.2.2",
        "selenium>=4.24.0",
        "tqdm>=4.66.5",
        "requests>=2.32.3",
        "lxml>=5.3.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Licesnse :: MIT License",
        "Operating System :: OS Independent",
    ],
)
