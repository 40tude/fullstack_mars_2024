from pathlib import Path
import logging
import scrapy
from scrapy.crawler import CrawlerProcess


class RandomQuoteSpider(scrapy.Spider):
    name = "randomquote"
    start_urls = [
        "http://quotes.toscrape.com/random",
    ]

    def parse(self, response):
        return {
            "text": response.xpath(
                "/html/body/div/div[2]/div[1]/div/span[1]/text()"  # En dehors de text() on peut mettre quoi ?
            ).get(),
            "author": response.xpath(
                "/html/body/div/div[2]/div[1]/div/span[2]/small/text()"
            ).get(),
            "tags": response.xpath(
                "/html/body/div/div[2]/div[1]/div/div/a/text()"
            ).getall(),
            # difference entre get() et getall()
            # .get() always returns a single result
            #     if there are several matches, content of a first match is returned;
            #     if there are no matches, None is returned.
            # .getall() returns a list with all results.
        }


filename = "1_randomquote.json"
current_dir = Path(__file__).parent

# If file already exists, delete it before crawling
# Otherwise Scrapy concatenate the results
if Path.exists(current_dir / filename):
    (current_dir / filename).unlink()

# https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(
    settings={
        "USER_AGENT": "Chrome/97.0",
        "LOG_LEVEL": logging.INFO,  # CRITICAL, ERROR, WARNING, INFO, DEBUG...
        # https://docs.scrapy.org/en/latest/topics/logging.html#topics-logging
        "FEEDS": {
            str(current_dir)
            + "/"
            + filename: {
                "format": "json"
            },  # https://docs.scrapy.org/en/latest/topics/feed-exports.html#std-setting-FEEDS
        },
    }
)

process.crawl(RandomQuoteSpider)
process.start()
