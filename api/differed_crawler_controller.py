import json
from http import HTTPStatus

from flask import Response as FlaskResponse
from flask import request

from dto.controller_responses import ControllerResponses
from dto.differed_crawling_info import DifferedCrawlingInfo
from helpers.logger import logger
from service.differed_crawling_service import DifferedCrawlingService
from service.differed_parsing_service import DifferedParsingService
from . import routes


@routes.route("/differed_crawler/", methods=["POST"])
def differed_crawler_controller():
    logger.info('Starting differed crawling process')
    crawling_info = DifferedCrawlingInfo(**json.loads(request.data))
    differed_crawling_service = DifferedCrawlingService(crawling_info)
    pages_to_crawl = differed_crawling_service.get_pages_to_crawl()
    if pages_to_crawl == 0:
        logger.error(f'An error occurred while retrieven pages to crawl. No pages were crawled')
        return FlaskResponse(json.dumps(ControllerResponses.NO_CRAWLED_PAGES, default=lambda o: o.__dict__),
                             status=HTTPStatus.BAD_REQUEST)

    crawled_pages = differed_crawling_service.crawl_pages()
    if crawled_pages == 0:
        logger.error(f'An error occurred during html crawling. No pages were crawled')
        return FlaskResponse(json.dumps(ControllerResponses.NO_CRAWLED_PAGES, default=lambda o: o.__dict__),
                             status=HTTPStatus.BAD_REQUEST)

    extracted_elements_count = DifferedParsingService(crawling_info).parse_crawled_items()
    if extracted_elements_count == 0:
        logger.error(f'An error occurred during html parsing. No item could be parsed')
        return FlaskResponse(json.dumps(ControllerResponses.NO_PARSED_ITEMS, default=lambda o: o.__dict__),
                             status=HTTPStatus.BAD_REQUEST)

    crawled_pages = 7
    return FlaskResponse(json.dumps({
        'status': 'success',
        'message': f'Crawled {crawled_pages} successfully and extracted {extracted_elements_count} items'
    }, default=lambda o: o.__dict__), status=HTTPStatus.OK)
