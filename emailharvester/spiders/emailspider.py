import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urlparse
import re
from ..items import EmailPhoneItem
from ..itemsloaders import EmailPhoneItemLoader

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
                for line in f.readlines():
                    self.allowed_domains.append(line.strip())
                    self.urls.append(f"http://{line.strip()}")
    def start_requests(self):
        # Yield a request for each domain
        for url in self.urls:
            yield scrapy.Request(url=url,callback=self.parse,meta={"domain":urlparse(url).netloc})

    def parse(self, response):
        emailPhone = EmailPhoneItemLoader(item = EmailPhoneItem(),selector = response)
        emailPhone.add_value("domain",response.meta.get("domain"))
        emailPhone.add_value("emails",response)
        emailPhone.add_value("phones",response)
        yield emailPhone.load_item()
