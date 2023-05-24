import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urlparse
import re
from ..items import EmailPhoneItem
from ..itemsloaders import EmailPhoneItemLoader
# def find_

class EmailSpider(CrawlSpider):
    name = "emailspider"
    allowed_domains = []
    urls = []
    rules = (
        Rule(LinkExtractor(allow=re.compile(r"contact[/\-]*(us)?|about[/\-]*(us)?")),callback="parse", follow=True),
    )

    def __init__(self, domain_file=None, *args, **kwargs):

        super(EmailSpider, self).__init__(*args, **kwargs)
        if domain_file is not None:
            with open(domain_file, 'r') as f:
                for line in f:
                    parsedURL = urlparse(line)
                    self.allowed_domains.append(parsedURL.netloc)
                    self.urls.append(f"https://{parsedURL.netloc}{parsedURL.path}?{parsedURL.query}")

    def start_requests(self):
        # Yield a request for each domain
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        emailPhone = EmailPhoneItemLoader(item = EmailPhoneItem(),selector = response)
        emailPhone.add_value("domain",urlparse(response.url).netloc)
        emailPhone.add_value("emails",response)
        emailPhone.add_value("phones",response)
        yield emailPhone.load_item()
