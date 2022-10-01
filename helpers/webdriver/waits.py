import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from helpers.logger import logger


def wait_presence_of_element_located(driver, timeout, selector_type, element_identifier, message=''):
    selector_type = selector_type.upper()
    if selector_type == 'ID':
        return _wait_presence_of_element_located_by_id(driver, timeout, element_identifier, message)
    if selector_type == 'XPATH':
        return _wait_presence_of_element_located_by_xpath(driver, timeout, element_identifier, message)

    raise NotImplementedError(f'No WaitPresenceOfElementLocated implementation for selector_type: {selector_type}')


def _wait_presence_of_element_located_by_id(driver, timeout, descriptor_property, message=''):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, descriptor_property)), message)


def _wait_presence_of_element_located_by_xpath(driver, timeout, descriptor_property, message=''):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, descriptor_property)), message)


def _wait_visibility_of_element_located_by_xpath(driver, timeout, descriptor_property, message=''):
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, descriptor_property)), message)


def _wait_visibility_of_element_located_by_id(driver, timeout, descriptor_property, message=''):
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, descriptor_property)), message)


def wait_visibility_of_element_located(driver, timeout, selector_type, descriptor_property, message=''):
    selector_type = selector_type.upper()
    if selector_type == 'ID':
        return _wait_visibility_of_element_located_by_id(driver, timeout, descriptor_property, message)
    if selector_type == 'XPATH':
        return _wait_visibility_of_element_located_by_xpath(driver, timeout, descriptor_property, message)

    raise NotImplementedError(f'No WaitVisibilityOfElementLocated implementation for selector_type: {selector_type}')


def wait_until_page_ready(driver, timeout, period_for_check=0.1, throw_error=True):
    waiting_time = 0
    page_ready = is_document_really_completed(driver)

    while waiting_time < timeout and not page_ready:
        print_page_status(driver)
        waiting_time = waiting_time + (period_for_check * 1000)
        time.sleep(period_for_check)
        page_ready = is_document_really_completed(driver)

    print_page_status(driver)

    if not page_ready:
        ajax_status = 'JQuery is loaded with {} active requests'.format(driver.execute_script("return $.active")) \
            if is_jquery_loaded(driver) else 'JQuery is NOT loaded jet'

        msg = 'Timed out waiting for page ready. State {}, Ajax status: {}'.format(
            driver.execute_script("return document.readyState"), ajax_status)
        if throw_error:
            raise Exception(msg)
        else:
            logger.warn(msg)
        return False
    else:
        return True


def print_page_status(driver):
    document_completed = is_document_completed(driver)
    jquery_loaded = is_jquery_loaded(driver)
    all_ajax_completed = jquery_loaded and is_all_ajax_completed(driver)
    logger.info('document_completed: {} | jquery_loaded: {} | all_ajax_completed: {}'
                .format(document_completed, jquery_loaded, all_ajax_completed))


def is_document_really_completed(driver):
    document_completed = is_document_completed(driver)
    jquery_loaded = is_jquery_loaded(driver)
    all_ajax_completed = jquery_loaded and is_all_ajax_completed(driver)
    return document_completed and all_ajax_completed


def is_document_completed(driver):
    return driver.execute_script("return document.readyState") == 'complete'


def is_jquery_loaded(driver):
    return driver.execute_script("return typeof $ !== 'undefined'")


def is_all_ajax_completed(driver):
    return driver.execute_script("return $.active") == 0
