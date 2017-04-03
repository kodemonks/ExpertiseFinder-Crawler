# -*- coding: utf-8 -*-
from scrapy import signals
from scrapy.exporters import CsvItemExporter


#Override default CSV writer method
#provided by scrapy to have extra SCV handling functionality
#Change here for File name - CSV Header (Format + visibility )
class CSVPipeline(object):

#Init method
  def __init__(self):
    self.files = {}




#override existing properties
#and pass crawler item when process starts
  @classmethod
  def from_crawler(cls, crawler):
    pipeline = cls()
    crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    return pipeline



#Only method that needs to be edited in this class
#
  def spider_opened(self, spider):
    file = open('%s_data.csv' % spider.name, 'w+b')
    self.files[spider] = file
    self.exporter = CsvItemExporter(file)
    self.exporter.fields_to_export = [
    'Name',
    'University',
    'Job_Title',
    'Department',
    'Email',
    'City',
    'State',
    'url',
    'Phone'
]

    self.exporter.start_exporting()

#Spider close method
  def spider_closed(self, spider):
    self.exporter.finish_exporting()
    file = self.files.pop(spider)
    file.close()

#Spider process item method
  def process_item(self, item, spider):
    self.exporter.export_item(item)
    return item