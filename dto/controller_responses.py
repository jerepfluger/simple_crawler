import json
from enum import Enum

BASE_RESPONSE = "{'status': {}, 'message': {}}"


class ControllerResponses(Enum):
    NO_CRAWLED_PAGES = json.loads(BASE_RESPONSE.format('failed', 'No pages were crawled'))
    NO_PARSED_ITEMS = json.loads(BASE_RESPONSE.format('failed', 'No item could be parsed'))
