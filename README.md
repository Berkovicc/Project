This project provides three scrapers written with BeautifulSoup4, Selenium and Scrapy modules. 

Berk Arıkan - 437954 - b.arikan@student.uw.edu.pl

# Usage
You can install requirements via pip.
`pip install -r requirements.txt`

Then, to run bs4 scraper as:

`python soup_scraper_stackoverflow.py`

To run Selenium scraper, you need driver for Chrome which is given at selenium folder and it must be at the same directory as scraper:

`python selenium_scraper_stackoverflow`

To run Scrapy scraper, you need scrapy binary:

`scrapy runspider scrapy_scraper_stackoverflow.py`