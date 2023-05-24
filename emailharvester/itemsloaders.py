from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader
from .items import EmailPhoneItem
import re

def deobfuscate_protected_email(obfuscated_email):
    XOR_key = int(obfuscated_email[:2],16)
    email = ""
    for i in range(2,len(obfuscated_email),2):
        email += chr(int(obfuscated_email[i:i+2],16) ^ XOR_key)
    return email
def is_valid_email(email):
    mo = re.match(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}",email)
    return bool(mo)
def find_emails(response):
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", response.text)
    emails = set(emails)
    if len(emails) == 0:
        for anchor in response.xpath("//a[contains(@href,'email-protection')]"):
            cf_email = anchor.attrib["href"].split("#")
            if len(cf_email) == 1:
                cf_email = anchor.attrib["data-cfemail"]
            else:
                cf_email = cf_email[-1]
            email = deobfuscate_protected_email(cf_email)
            if is_valid_email(email):
                emails.update({email})
    return emails

def find_phones(response):
    phones = set()
    for phone in response.xpath("//a[contains(@href,'tel')]/@href").getall():
        mo = re.search(r"[\(\)\d\s\-\+]+",phone)
        if mo is not None:
            number = mo.group()
            if not (number in phones):
                phones.update({number})
    return phones

class EmailPhoneItemLoader(ItemLoader):
    default_class_item = EmailPhoneItem
    # default_output_processor = TakeFirst()
    domain_out = TakeFirst()
    emails_in = MapCompose(find_emails)
    phones_in = MapCompose(find_phones)