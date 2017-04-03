# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# -*- coding: utf-8 -*-

from scrapy.item import Item,Field

#Item Class to store Data Model
#All items are stored here in this class
#Dictionary type struture
# similar to Model class of MVC

class ExpertiseInfoItem(Item):
    University = Field()
    Name=Field()
    Job_Title=Field()
    Department=Field()
    Email=Field()
    City=Field()
    State=Field()
    url = Field()
    Phone=Field()