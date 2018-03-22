import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from migration.items import MigrationItem
from migration.items import DrugiItem



from readability.readability import Document
import urllib
import html2text
class PitSpider(scrapy.Spider):
    name='articles'
    allowed_domains = ["agencjawhites.pl"]
    start_urls = [
        "https://agencjawhites.pl/"
        ]

    def parse(self, response):
        for page in response.css('.entry-title'):
            yield{
            'name': page.css('h3 a::text').extract_first()
            }
class WhtsSpider(CrawlSpider):
    name='whts'
    allowed_domains = ['babcine.pl']
    start_urls = ['http://babcine.pl']
    rules = (
        Rule(LinkExtractor(allow=('babcine.pl')),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        self.log('Scrapping: ' + response.url)
        print('Processing..' + response.url)
        hxs = HtmlXPathSelector(response)
        sample = hxs.select("//body").extract_first()

        converter = html2text.HTML2Text()
        converter.ignore_links = True
        print(converter.handle(sample)) #Python 3 print syntax
        articles = response.xpath('//a')

        for article in articles:
            item = MigrationItem()
            item['link_title']=article.xpath('text()').extract_first()
            item['url']=article.xpath('@href').extract_first()

            yield item
        #title = response.css('.entry-title::text').extract_first()
        #post = response.css('.white-article').extract_first()
        #print('Title: %s \n' % title)
        #print('Content: %s \n' % post)

class newCrawler(CrawlSpider):
    name='az'
    allowed_domains = ['babcine.pl']
    start_urls = ['http://babcine.pl']
    rules = (
        Rule(LinkExtractor(allow=('babcine.pl'), canonicalize=True, unique=True),
             callback="parse_items",
             follow=True),)
    def parse_items(self, response):
        item = DrugiItem()
        item['url']=response.url

        converter = html2text.HTML2Text()
        converter.ignore_links = True
        item['text']=converter.handle(response.css('.entry-content').extract_first())

        return item

class newCrawler(CrawlSpider):
    name='pit'
    allowed_domains = ['pit.pl']
    start_urls = ['http://www.pit.pl']
    rules = (
        Rule(LinkExtractor(allow=('pit.pl/.*\d+/$'), canonicalize=True, unique=True),
             callback="parse_items",
             follow=True),)
    def parse_items(self, response):
        item = DrugiItem()
        item['url']=response.url

        converter = html2text.HTML2Text()
        converter.ignore_links = True
        item['text']=converter.handle(response.css('section.lev2').extract_first())

        return item
