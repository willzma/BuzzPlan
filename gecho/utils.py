'''
Some utility functions that may be applicable to any page.
'''

nums = {'zero': 0, 
        'one': 1, 
        'two': 2, 
        'three': 3, 
        'four': 4, 
        'five': 5, 
        'six': 6, 
        'seven': 7, 
        'eight': 8, 
        'nine': 9, 
        'ten': 10}


def str2int(text):
    '''
    Is this Natural Language Processing? Converts words one through ten to 1-10. Ignores case.
    e.g. 'Ten' returns 10.
    '''
    return nums[text.lower()]


def asciify_spaces(str):
    '''
    Most table data is originally in a UTF-8 format using xa0 as an unbreakable space.
    This function normalizes that into an ASCII spaces for correspondence with user input.
    '''
    return str.replace(u'\xa0', ' ')


def urlify_spaces(str):
    '''
    When spaces are passed in as part of a URL, they are encoded as %20.
    This function does just that.
    '''
    return str.replace(' ', '%20')


def get_hrefs(container):
    '''
    Goes through each element and digs down until finding an href, otherwise skipping.
    Useful for concentration/thread pages which are basically just text and hrefs.
    '''
    hrefs, node_queue = [], [container]
    while node_queue:
        node = node_queue.pop(0)
        if 'href' in node.attrib:
            hrefs.append(node.attrib['href'])
        node_queue.extend(node)
    return hrefs