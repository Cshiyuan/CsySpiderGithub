
from scrapy.item import Item, Field


class StackItem(Item):
    title = Field()
    url = Field()
