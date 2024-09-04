from setuptools import setup

setup(
    name="yfscraper",
    version="0.1.0",
    description="Tool for scraping stock data from yahoo.com",
    url="https://github.com/adam42739/yf-scraper",
    author="Adam Lynch",
    author_email="aclynch@umich.edu",
    license="MIT License",
    packages=["yfscraper"],
    install_requires=["pandas>=2.2.2", "selenium>=4.24.0", "tqdm>=4.66.5"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Licesnse :: MIT License",
        "Operating System :: OS Independent",
    ],
)
