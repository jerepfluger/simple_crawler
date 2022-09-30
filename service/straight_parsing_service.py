from helpers.logger import logger
from os import listdir
from os.path import isfile, join


class StraightParsingService:
    def __init__(self):
        self.files = None

    def parse_crawled_items(self, crawling_info):
        logger.info(f'Start parsing process of files located in {crawling_info["bot_name"]}')
        self.files = self.get_files_list(crawling_info['bot_name'])
        self.initialize_results_file(crawling_info['bot_name'])
        if not len(self.files) > 0:
            # TODO: Here we should raise an exception or handle this type of error. It would be a weird scenario
            # because we're validating this in a previous step. But just in case we'll handle it
            pass
        extracted_items_count = 0
        for file in self.files:
            extracted_items = 0
            try:
                extracted_items = self.process_file(file)
            except:
                pass
            extracted_items_count += extracted_items

        return extracted_items_count

    def get_files_list(self, folder_name):
        """
        returns a list of the files that are contained in the bot folder and need to be parsed
        :param folder_name: String
        :return: List[String]
        """
        # TODO: We need to add proper validations in here
        return [f for f in listdir(folder_name) if isfile(join(folder_name, f))]

    def initialize_results_file(self, bot_name):
        """
        In this method we'll create the output file that will be send to the client
        It'll be a csv file at first. Inside the method we'll just create the file as
        <bot_name>_results.csv and we'll continuously add parsed information
        :param param: String
        :return: None
        """
        pass

    def process_file(self, file_name):
        """
        Is the proper file parsing. We need here the detail of the data we want to extract
        The method will return the number of successfully parsed items
        :param file_name:
        :return: Integer
        """
        pass
