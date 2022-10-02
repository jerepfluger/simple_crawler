import re


def get_cleaner(cleaner):
    if cleaner.lower() == 'price':
        return clean_price

    return NotImplementedError(f'No Cleaner implementation for {cleaner}')


def clean_price(string):
    """
    """
    r = 0
    # avoid parsing an empty string or a string that does not contain a number
    if string is not None and any(i.isdigit() for i in string):
        (miles, decimal) = resolve_separators(string)
        r = string.replace(miles, '')
        r = r.replace(decimal, '.')
        r = str(re.findall('\d+', r)[-1])  # the last result
        if is_number(r):
            r = float(r)

    return r


def resolve_separators(num_string):
    decimal = ","
    miles = "."

    def opposite_delimiter(delimiter):
        return "." if delimiter == "," else ","

    if num_string is not None:
        reverse_input = num_string[::-1]
        possible_delimiters = '[.,]'
        search_delimiter = re.search(possible_delimiters, num_string)

        if search_delimiter:
            first_delimiter = search_delimiter.group(0)
            last_delimiter = re.search(possible_delimiters, reverse_input).group(0)
            if first_delimiter == last_delimiter:
                decimal, miles = (first_delimiter, opposite_delimiter(first_delimiter)) \
                    if re.search('^.*([{}]\d{{1,2}})$'.format(first_delimiter), num_string) \
                    else (opposite_delimiter(first_delimiter), first_delimiter)
            else:
                decimal, miles = (last_delimiter, first_delimiter)

    return miles, decimal


def is_number(s):
    try:
        float(s)
        return True
    except:
        return False
