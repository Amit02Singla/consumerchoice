# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv

class SinglepagespiderPipeline(object):
    def process_item(self, item, spider):
        return item

'''class CsvPipeline(object):

    def __init__(self):
        self.writer = csv.writer(open('pipelinecsv.csv', 'a'), lineterminator='\n')

    def process_item(self, item, spider):
        for i in item:
            print i
            self.writer.writerow(i)
        return item'''