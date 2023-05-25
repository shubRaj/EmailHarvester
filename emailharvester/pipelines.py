# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class EmailharvesterPipeline:
    def process_item(self, item, spider):
        phones_seen = set()
        adapter = ItemAdapter(item)
        if adapter.get("emails") is None:
            adapter["emails"] = []
        if adapter.get("phones") is None:
            adapter["phones"] = []
        else:
            """
                remove duplicate numbers
            """
            matches = []
            found = False
            for phone in adapter.get("phones"):
                for match in matches:
                    if match[-4] in phone:
                        found = True
                        break
                if not found:
                    phones_seen.update({phone})
                    """Filter based on last digits"""
                    mo = re.search(r"\d+$",phone)
                    if mo:
                        matches.append(mo.group())
            adapter["phones"] = phones_seen
        return item
