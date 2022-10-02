def get_multiple_items(item, selector_type, element_identifiers, cleaner_item=None, **kwargs):
    selector_type = selector_type.upper()
    if selector_type == 'XPATH':
        return get_items_by_xpath(item, element_identifiers, cleaner_item, **kwargs)

    raise NotImplementedError(f'No GetMultipleItems implementation for selector_type: {selector_type}')


def get_items_by_xpath(item, xpath, cleaner_item=None, **kwargs):
    try:
        if 'format_str' in kwargs.keys():
            xpath = xpath.format(kwargs["format_str"])
        r = item.xpath(xpath)
        if cleaner_item is not None:
            r = cleaner_item(r)

        if len(r) > 0:
            return r
    except:
        pass


def get_item_by_attrib(item, attrib, cleaner_item=None, **kwargs):
    try:
        if 'format_str' in kwargs.values():
            attrib = attrib.format(kwargs["format_str"])
        r = item.attrib[attrib]
        if cleaner_item is not None:
            r = cleaner_item(r)

        if r is not None:
            return r
    except:
        pass


def get_single_item(item, selector_type, element_identifier, cleaner_item=None, **kwargs):
    selector_type = selector_type.upper()
    if selector_type == 'XPATH':
        return get_item_by_xpath(item, element_identifier, cleaner_item, **kwargs)

    raise NotImplementedError(f'No GetSingleItem implementation for selector_type: {selector_type}')


def get_item_by_xpath(item, xpath, cleaner_item=None, **kwargs):
    try:
        if 'format_str' in kwargs.values():
            xpath = xpath.format(kwargs["format_str"])
        r = item.xpath(xpath)[0]
        if cleaner_item is not None:
            r = cleaner_item(r)

        if r is not None:
            return r
    except:
        pass
