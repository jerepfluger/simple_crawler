class DifferedCrawlingInfo:
    def __init__(self, browser_type, bot_name, crawl_url, information_selector_type, html_information_location,
                 html_information_attribute_identifier, inner_html_information_location, next_page_policy,
                 next_page_selector_type, next_page_location, complete_crawl_url, scrolling_needs_click,
                 scrolling_timeout, parsing_items):
        self.browser_type = browser_type
        self.bot_name = bot_name
        self.crawl_url = crawl_url
        self.information_selector_type = information_selector_type
        self.html_information_location = html_information_location
        self.html_information_attribute_identifier = html_information_attribute_identifier
        self.inner_html_information_location = inner_html_information_location
        self.next_page_policy = next_page_policy
        self.next_page_selector_type = next_page_selector_type
        self.next_page_location = next_page_location
        self.complete_crawl_url = complete_crawl_url
        self.scrolling_needs_click = scrolling_needs_click
        self.scrolling_timeout = scrolling_timeout
        self.parsing_items = parsing_items
