from selenium.webdriver.common.by import By


def find_elements(driver, selector_type, element_identifier):
    selector_type = selector_type.upper()
    if selector_type == 'ID':
        return driver.find_elements(By.ID, element_identifier)
    if selector_type == 'XPATH':
        return driver.find_elements(By.XPATH, element_identifier)

    raise NotImplementedError(f'No FindElementsBy implementation for selector_type: {selector_type}')


def find_element(driver, selector_type, element_identifier):
    selector_type = selector_type.upper()
    if selector_type == 'ID':
        return driver.find_element(By.ID, element_identifier)
    if selector_type == 'XPATH':
        return driver.find_element(By.XPATH, element_identifier)

    raise NotImplementedError(f'No FindElementBy implementation for selector_type: {selector_type}')


def find_element_and_click_it_with_javascript(driver, selector_type, element_identifier):
    element = find_element(driver, selector_type, element_identifier)
    driver.execute_script('arguments[0].click();', element)


def find_element_by_id_and_send_keys(driver, element_identifier, keys):
    _find_element_and_send_keys(driver, By.ID, element_identifier, keys)


def find_element_by_xpath_and_send_keys(driver, element_identifier, keys):
    _find_element_and_send_keys(driver, By.XPATH, element_identifier, keys)


def _find_element_and_send_keys(driver, selector_type, element_identifier, keys):
    element = driver.find_element(selector_type, element_identifier)
    for key in keys:
        element.send_keys(key)


def find_element_by_id_and_click_it_with_javascript(driver, element_identifier):
    _find_element_and_click_it_with_javascript(driver, By.ID, element_identifier)


def find_element_by_xpath_and_click_it_with_javascript(driver, element_identifier):
    _find_element_and_click_it_with_javascript(driver, By.XPATH, element_identifier)


def _find_element_and_click_it_with_javascript(driver, selector_type, element_identifier):
    element = driver.find_element(selector_type, element_identifier)
    driver.execute_script("arguments[0].click();", element)
