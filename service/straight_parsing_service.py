import csv
from lxml import etree

from config.config import settings as config_file
from helpers.cleaners import get_cleaner
from helpers.files_helper import create_folder_if_not_exists
from helpers.logger import logger
from os import listdir
from os.path import isfile, join

from helpers.parser.file_parser_helper import get_items_by_xpath, get_multiple_items, get_single_item


class StraightParsingService:
    def __init__(self, crawling_info):
        self.crawling_info = crawling_info
        self.config = config_file.crawling
        self.files = None

    def parse_crawled_items(self):
        logger.info(f'Start parsing process of files located in {self.crawling_info.bot_name}')
        logger.info('Getting file list to parse')
        self.get_files_list()
        logger.info('Initializing csv results file')
        self.initialize_results_file()
        if not len(self.files) > 0:
            raise Exception('No files found to parse')
        extracted_items_count = 0
        for file in sorted(self.files):
            extracted_items = 0
            try:
                extracted_items = self.process_file(file)
            except:
                pass
            extracted_items_count += extracted_items

        return extracted_items_count

    def get_files_list(self):
        """
        returns a list of the files that are contained in the bot folder and need to be parsed
        """
        folder_name = f'{self.config["data_base_path"]}/{self.crawling_info.bot_name}'
        self.files = [f for f in listdir(folder_name) if isfile(join(folder_name, f))]

    def initialize_results_file(self):
        """
        In this method we'll create the output file that will be send to the client. It'll be a csv file at first.
        Inside the method we'll just create the file as <bot_name>_results.csv and we'll continuously add parsed information
        """
        folder_name = f'{self.config["data_base_path"]}/{self.crawling_info.bot_name}/results'
        create_folder_if_not_exists(folder_name)
        with open(f'{folder_name}/results.csv', 'w+') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(list(self.crawling_info.parsing_items.keys()))

    def process_file(self, file_name):
        """
        Is the proper file parsing. We need here the detail of the data we want to extract
        The method will return the number of successfully parsed items
        """
        folder_name = f'{self.config["data_base_path"]}/{self.crawling_info.bot_name}'
        with open(f'{folder_name}/{file_name}', 'r+') as file:
            html_source = file.read()
        html = etree.HTML(html_source)

        html_items = get_multiple_items(html, self.crawling_info.information_selector_type, self.crawling_info.inner_html_information_location)
        items_count = 0
        for item in html_items:
            csv_line = []
            for key in self.crawling_info.parsing_items.keys():
                try:
                    cleaner = None
                    if self.crawling_info.parsing_items[key].get('cleaner') is not None:
                        cleaner = get_cleaner(self.crawling_info.parsing_items[key]['cleaner'])
                    element = get_single_item(item, self.crawling_info.parsing_items[key]['selector_type'], self.crawling_info.parsing_items[key]['element_identifier'], cleaner_item=cleaner)
                    csv_line.append(element)
                except:
                    csv_line.append('')
            folder_name = f'{self.config["data_base_path"]}/{self.crawling_info.bot_name}/results'
            with open(f'{folder_name}/results.csv', 'a+') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(csv_line)
            items_count += 1

        return items_count
