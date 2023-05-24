# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class EmailharvesterPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("emails") is None:
            adapter["emails"] = []
        if adapter.get("phones") is None:
            adapter["phones"] = []
        return item
