# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from datetime import datetime

import pandas as pd
from scrapy.exporters import CsvItemExporter


class Question3Pipeline:
    '''Pipeline to save ArtItems in csv file and as pickled DataFrame'''

    def __init__(self):
        '''Initialise CsvItemExporter and start exporting ArtItems'''
        self.filename = f"question_3_{str(datetime.today().strftime('%d-%m-%Y'))}.csv"
        self.csv_file = open(self.filename, 'wb')
        self.csv_file_exporter = CsvItemExporter(self.csv_file)
        self.csv_file_exporter.start_exporting()

    def close_spider(self, spider):
        '''Finish exporting ArtItems, close csv, create and
            pickle DataFrame'''
        self.csv_file_exporter.finish_exporting()
        self.csv_file.close()
        self.question_3_df = pd.read_csv(self.filename)
        self.question_3_df.to_pickle('question_3_df.pkl')

    def process_item(self, item, spider):
        '''Process ArtItems'''
        self.csv_file_exporter.export_item(item)
        return item
