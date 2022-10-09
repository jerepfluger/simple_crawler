import time

from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config.config import settings as config_file
from exceptions.exceptions import NoMorePagesException
from helpers.files_helper import create_folder_if_not_exists, create_file_if_not_exists
from helpers.logger import logger
from helpers.webdriver.find_element import find_elements, find_element, find_element_and_click_it_with_javascript
from helpers.webdriver.waits import wait_presence_of_element_located
from webdrivers.webdriver import WebDriver


class DifferedCrawlingService:
    def __init__(self, crawling_info):
        self.crawling_info = crawling_info
        self.driver = WebDriver().acquire(self.crawling_info.browser_type)
        self.driver.maximize_window()
        self.config = config_file.crawling
        self.folder_name = f'{self.config["data_base_path"]}/{self.crawling_info.bot_name}'
        self.save_html_page_items_counter = 40

    def get_pages_to_crawl(self):
        logger.info(f'Starting differed crawling process for {self.crawling_info.bot_name}')
        create_folder_if_not_exists(self.folder_name)
        create_file_if_not_exists(self.folder_name, 'urls')
        logger.info('Directory for storing html content is clean and empty')

        logger.info(f'Browser GET: {self.crawling_info.crawl_url}')
        self.driver.get(self.crawling_info.crawl_url)
        wait_presence_of_element_located(self.driver, 5, self.crawling_info.information_selector_type,
                                         self.crawling_info.html_information_location)

        if self.crawling_info.next_page_policy.lower() == 'scrolling':
            logger.info('Next page policy set to scrolling')
            pages_count = self.handle_scrolling_policy()
        elif self.crawling_info.next_page_policy.lower() == 'paging':
            logger.info('Next page policy set to paging')
            pages_count = self.handle_paging_policy()
        else:
            raise NotImplementedError(f'Paging policy {self.crawling_info.next_page_policy} not implemented')

        logger.info(f'Crawled a total of {pages_count} pages')
        return pages_count

    def handle_scrolling_policy(self):
        # TODO: Test if having all elements in memory is suitable or if we should store them as we crawl them
        scrolling_count = 0
        while True:
            logger.info(f'Current scrolling count is {scrolling_count}')
            elements = find_elements(self.driver, self.crawling_info.information_selector_type,
                                     self.crawling_info.html_information_location)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", elements[-1])
            try:
                logger.info('Scrolling to last item if possible')
                if self.crawling_info.scrolling_needs_click:
                    element = find_element(self.driver, self.crawling_info.next_page_selector_type,
                                           self.crawling_info.next_page_location)
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    find_element_and_click_it_with_javascript(self.driver, self.crawling_info.next_page_selector_type,
                                                              self.crawling_info.next_page_location)
                self.driver.execute_script(f'window.scrollTo(0, {int(elements[-1].rect["y"]) + 100})')
                time.sleep(self.crawling_info.scrolling_timeout)
                if not len(elements) < len(find_elements(self.driver, self.crawling_info.information_selector_type,
                                                         self.crawling_info.html_information_location)):
                    logger.info('No new elements detected. Finishing scrolling')
                    break
                scrolling_count += 1
            except NoSuchElementException as ex:
                logger.exception('Unable to find element', ex)
                break
        logger.info(f'Scrolled a total of {scrolling_count} times. Saving html content now')
        self.save_urls()

        return scrolling_count

    def handle_paging_policy(self):
        pages_count = 0
        try:
            while True:
                logger.info(f'Saving html content for page {pages_count + 1}')
                self.save_urls()
                pages_count += 1
                logger.info(f'Selecting page {pages_count + 1} if exists')
                self.next_page(pages_count)
        except NoMorePagesException:
            logger.info(f'We\'ve reached the final page over a total count of {pages_count}')

        return pages_count

    def crawl_pages(self):
        create_folder_if_not_exists(f'{self.folder_name}/results')
        urls_location = f'{self.folder_name}/urls'
        crawled_pages = 0
        with open(urls_location, 'r+') as urls_file:
            while True:
                line = urls_file.readline()
                if line.endswith('\n'):
                    line = line[:-1]
                if not line:
                    break

                logger.info(f'Browser GET: {line}')
                self.driver.get(f'{self.crawling_info.complete_crawl_url}{line}')
                self.save_html(self.crawling_info.inner_html_information_location, crawled_pages, line)
                crawled_pages += 1

        return crawled_pages

    def save_urls(self):
        urls = find_elements(self.driver, self.crawling_info.information_selector_type,
                             self.crawling_info.html_information_location)
        for count, url in enumerate(urls, start=1):
            if self.crawling_info.html_information_attribute_identifier is not None:
                url = url.get_attribute(self.crawling_info.html_information_attribute_identifier)
            if not url.endswith('\n'):
                url += '\n'
            with open(f'{self.folder_name}/urls', 'a+') as file:
                logger.info(f'Saving url {url} with a current total count of {count}')
                file.write(url)

    def save_html(self, html_container, pages_count, url=''):
        try:
            wait_presence_of_element_located(self.driver, self.crawling_info.scrolling_timeout,
                                             self.crawling_info.information_selector_type,
                                             self.crawling_info.inner_html_information_location)
        except TimeoutException:
            logger.error(f'Timeout waiting for html main locator for url {url}. Skipping element')
            return
        located_element = find_element(self.driver, self.crawling_info.information_selector_type, html_container)
        element_html = located_element.get_attribute('innerHTML')
        with open(f'{self.folder_name}/results/page_{pages_count // self.save_html_page_items_counter}.gz',
                  'a+') as file:
            file.write(element_html)
            logger.info(f'Saved url element into results file.{"" if len(url) == 0 else " Url: {}".format(url)}')

    def next_page(self, page_number):
        try:
            wait_presence_of_element_located(self.driver, 5, self.crawling_info.next_page_selector_type,
                                             self.crawling_info.next_page_location)
            pages_element = find_elements(self.driver, self.crawling_info.next_page_selector_type,
                                          self.crawling_info.next_page_location)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", pages_element[0])
            for page in pages_element:
                if page.text is not None and page.text != '' and int(page.text) == page_number + 1:
                    self.driver.execute_script('arguments[0].click();', page)
                    return

            raise NoMorePagesException
        except (NoSuchElementException, TimeoutException):
            logger.error(
                f'Unable to find next page button with selector_type: {self.crawling_info.next_page_selector_type}'
                f' and next_page_location: {self.crawling_info.next_page_location}')
            raise NoMorePagesException
