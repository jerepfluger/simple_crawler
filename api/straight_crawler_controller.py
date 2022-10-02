import json
from http import HTTPStatus

from flask import Response as FlaskResponse
from flask import request

from dto.controller_responses import ControllerResponses
from dto.straight_crawling_info import StraightCrawlingInfo
from helpers.logger import logger
from service.straight_crawling_service import StraightCrawlingService
from service.straight_parsing_service import StraightParsingService
from . import routes


@routes.route("/straight_crawler/", methods=["POST"])
def straight_crawler_controller():
    crawling_info = StraightCrawlingInfo(**json.loads(request.data))
    crawled_pages = StraightCrawlingService(crawling_info).gather_html_information()
    if crawled_pages == 0:
        logger.error(f'An error occurred during straight html crawling. No pages were crawled')
        return FlaskResponse(json.dumps(ControllerResponses.NO_CRAWLED_PAGES, default=lambda o: o.__dict__),
                             status=HTTPStatus.INTERNAL_SERVER_ERROR)

    extracted_elements_count = StraightParsingService(crawling_info).parse_crawled_items()
    if extracted_elements_count == 0:
        logger.error(f'An error occurred during html parsing. No item could be parsed')
        return FlaskResponse(json.dumps(ControllerResponses.NO_PARSED_ITEMS, default=lambda o: o.__dict__),
                             status=HTTPStatus.INTERNAL_SERVER_ERROR)

    return FlaskResponse(json.dumps({
        'status': 'success',
        'message': f'Crawled {crawled_pages} successfully and extracted {extracted_elements_count} items'
    }, default=lambda o: o.__dict__), status=HTTPStatus.OK)
