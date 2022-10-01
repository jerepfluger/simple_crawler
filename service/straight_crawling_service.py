from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from exceptions.exceptions import NoMorePagesException
from helpers.logger import logger
from helpers.files_helper import create_folder_if_not_exists
from helpers.webdriver.find_element import find_element, find_element_and_click_it_with_javascript
from helpers.webdriver.waits import wait_presence_of_element_located
from webdrivers.webdriver import WebDriver


class StraightCrawlingService:
    def __init__(self):
        self.driver = None
        self.html_folder_location = None
        self.crawling_info = None

    def set_crawling_info(self, crawling_info):
        self.crawling_info = crawling_info

    def gather_html_information(self):
        self.driver = WebDriver().acquire(self.crawling_info['browser_type'])
        self.driver.maximize_window()
        create_folder_if_not_exists(self.crawling_info['bot_name'])

        logger.info(f'Browser GET: {self.crawling_info["crawl_url"]}')
        self.driver.get(self.crawling_info['crawl_url'])
        wait_presence_of_element_located(self.driver, 5, self.crawling_info['information_selector_type'],
                                         self.crawling_info['html_information_location'])

        if self.crawling_info['next_page_policy'].lower() == 'scrolling':
            pages_count = self.handle_scrolling_policy()
        elif self.crawling_info['next_page_policy'].lower() == 'paging':
            pages_count = self.handle_paging_policy()
        else:
            raise NotImplementedError(f'Paging policy {self.crawling_info["next_page_policy"]} not implemented')

        logger.info(f'Crawled a total of {pages_count} pages')
        return pages_count

    def handle_scrolling_policy(self):
        # TODO: Test if having all elements in memory is suitable or if we should store them as we crawl them
        scrolling_count = 0
        while True:
            self.driver.execute_script(
                f'window.scrollTo(0,$({self.crawling_info["inner_html_information_location"]}).last().offset().top)')
            elem_count = self.driver.execute_script(
                f'return document.querySelectorAll({self.crawling_info["inner_html_information_location"]}).length')
            try:
                WebDriverWait(self.driver, self.crawling_info['scrolling_timeout']).until(
                    lambda x: x.find_element_by_xpath(
                        "{}[{}]".format(self.crawling_info["inner_html_information_location"], elem_count + 1)))
                scrolling_count += 1
            except TimeoutException:
                logger.info('Finish scrolling using a waiting timeout: {} seconds'.format(
                    self.crawling_info['scrolling_timeout']))
                break
        self.save_html_content(self.crawling_info['html_information_location'], scrolling_count)

        return scrolling_count

    def handle_paging_policy(self):
        pages_count = 0
        try:
            while True:
                self.save_html_content(self.crawling_info['html_information_location'], pages_count)
                pages_count += 1
                self.next_page()
        except NoMorePagesException:
            logger.info(f'We\'ve reached the final page over a total count of {pages_count}')

        return pages_count

    def save_html_content(self, html_container, pages_count):
        # TODO: Maybe we could need a cleaner function to get rid of unwanted garbage
        # It could be something like receiving an array with the instructions for removing this garbage and we iterate
        # through it with something like driver.execute_script(
        # "Array.from(document.getElementsByClassName('sr--soldout-container')).forEach(e => e.classList.remove('sr--soldout-container'));"
        # )
        wait_presence_of_element_located(self.driver, 5, self.crawling_info['information_selector_type'],
                                         self.crawling_info['html_information_location'])
        located_element = find_element(self.driver, self.crawling_info['information_selector_type'], html_container)
        element_html = located_element.get_attribute('innerHTML')
        with open(f'{self.crawling_info["bot_name"]}/page_{pages_count + 1}.gz', 'a+') as file:
            file.write(element_html.encode('utf-8'))

    def next_page(self):
        try:
            wait_presence_of_element_located(self.driver, 5, self.crawling_info['next_page_selector_type'],
                                             self.crawling_info['next_page_location'])
            element = find_element(self.driver, self.crawling_info['next_page_selector_type'],
                                   self.crawling_info['next_page_location'])
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            find_element_and_click_it_with_javascript(self.driver, self.crawling_info['next_page_selector_type'],
                                                      self.crawling_info['next_page_location'])
        except (NoSuchElementException, TimeoutException):
            logger.error(
                f'Unable to find next page button with selector_type: {self.crawling_info["next_page_selector_type"]}'
                f' and next_page_location: {self.crawling_info["next_page_location"]}')
