from helpers.logger import logger
from webdrivers.webdriver import WebDriver


class DifferedCrawlingService:
    def __init__(self):
        self.driver = None
        self.html_folder_location = None

    def get_pages_to_crawl(self, crawling_info):
        self.driver = WebDriver().acquire(crawling_info['browser_type'])
        self.driver.maximize_window()
        self.create_urls_file(crawling_info['bot_name'])

        logger.info(f'Browser GET: {crawling_info["url"]}')
        self.driver.get(crawling_info['url'])

        next_page = True
        pages_count = 0
        while next_page:
            self.save_urls_to_crawl(crawling_info['html_information_location'], crawling_info['information_selector_type'])
            pages_count += 1
            next_page = self.next_page(crawling_info['next_page_policy'], crawling_info['next_page_location'], crawling_info['next_page_selector_type'])

        logger.info(f'Crawled a total of {pages_count} pages')
        return pages_count

    def create_urls_file(self, bot_name):
        """
        This method is in charge of creating a file names <bot_name>_urls where we'll place all urls
        that need to be crawled in next step
        :param param: String
        :return: None
        """
        pass

    def save_urls_to_crawl(self, html_information_location, information_selector_type):
        """
        This method is in charge of saving into the urls file all urls that'll be crawled in the next iteration
        :return: None
        """
        pass

    def next_page(self, next_page_policy, next_page_location, next_page_selector_type):
        """
        This method is in charge of setting the driver to the next page if exists
        It'll return True if there's a next page. Otherwise we'll return False, so crawling process ends
        :param next_page_location: String
        :param next_page_selector_type: String
        :return: Boolean
        """
        pass

    def crawl_pages(self, crawling_info):
        """
        This method is in charge of
        :param crawling_info:
        :return:
        """
        urls_location = '{}_urls'.format(crawling_info['bot_name'])
        crawled_pages = 0
        with open(urls_location, 'r+') as urls_file:
            while True:
                line = urls_file.readline()
                if not line:
                    break

                self.driver.get(line)
                self.save_html(crawling_info['html_information_location'], crawling_info['information_selector_type'])
                crawled_pages += 1

        return crawled_pages

    def save_html(self, html_information_location, information_selector_type):
        """
        This method is in charge of saving into a file the html content that'll be processed in the parser
        We need to extract the html block that contains the items we need to parse and save into a file
        :param html_information_location: String
        :param information_selector_type: String
        :return: None
        """
        pass
