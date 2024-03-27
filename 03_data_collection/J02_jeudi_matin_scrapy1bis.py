from pathlib import Path

## More info => https://docs.python.org/3/library/logging.html
import logging
import scrapy
from scrapy.crawler import CrawlerProcess


class RandomQuoteSpider(scrapy.Spider):
    # Name of your spider
    name = "randomquote"

    # Url to start your spider from
    start_urls = [
        "http://quotes.toscrape.com/random",
    ]

    # Callback function that will be called when starting your spider
    # It will get text, author and tags of the first <div> with class="quote"
    def parse(self, response):
        return {
            "text": response.xpath(
                "/html/body/div/div[2]/div[1]/div/span[1]/text()"
            ).get(),
            "author": response.xpath(
                "/html/body/div/div[2]/div[1]/div/span[2]/small/text()"
            ).get(),
            "tags": response.xpath(
                "/html/body/div/div[2]/div[1]/div/div/a/text()"
            ).getall(),
        }


filename = "1_randomquote.json"
current_dir = Path(__file__).parent

# If file already exists, delete it before crawling (because Scrapy will
# concatenate the last and new results otherwise)
if Path.exists(current_dir / filename):
    (current_dir / filename).unlink()

# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log
## FEEDS => Where the file will be stored
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(
    settings={
        "USER_AGENT": "Chrome/97.0",
        "LOG_LEVEL": logging.INFO,
        "FEEDS": {
            str(current_dir) + "/" + filename: {"format": "json"},
        },
    }
)

# Start the crawling using the spider you defined above
process.crawl(RandomQuoteSpider)
process.start()
