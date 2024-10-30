# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from dateparser import parse
from datetime import datetime

from unicodedata import category


class BlocketPipeline:

    # def open_spider(self, spider):
    #     self.file = open("items.jsonl", "w")
    #
    # def close_spider(self, spider):
    #     self.file.close()

    def process_item(self, item, spider):

        if item.get('url'):
            item['url'] = item['url'].strip().lower()

        if item.get('title'):
            item['title'] = item['title'].strip()

        if item.get('company'):
            item['company'] = item['company'].strip()

        if item.get('date_added'):
            item['date_added'] = self.convert_date(item['date_added'])

        if item.get('date_expires'):
            item['date_expires'] = self.convert_date(item['date_expires'])

        if item.get('location'):
            item['location'] = item['location'].strip()

        if item.get('category'):
            item['category'] = ', '.join([c.strip() for c in item['category']])

        if item.get('type'):
            item['type'] = ', '.join([t.strip() for t in item['type']])

        if item.get('description'):
            item['description'] = '\n'.join([d.strip() for d in item['description']])

        return item

    @staticmethod
    def convert_date(swedish_date: str) -> str | None:
        if len(swedish_date.split()) == 2:
            swedish_date = f"{swedish_date} {datetime.now().year}"
        date_obj = parse(swedish_date, languages=['sv'])
        return date_obj.strftime("%Y-%m-%d") if date_obj else None

