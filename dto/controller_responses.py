import json
from enum import Enum

BASE_RESPONSE = "{'status': {}, 'message': {}}"


class ControllerResponses(Enum):
    NO_CRAWLED_PAGES = {'status': 'failed', 'message': 'No pages were crawled'}
    NO_PARSED_ITEMS = {'status': 'failed', 'message': 'No item could be parsed'}
