'''
Functions for doing course lookups in the catalog.
'''

from config import catalog_url, courses_href, search_href, unique_abbrs, unique_abbr_hrefs
from config import supported_degrees, degree_code_ranges
from utils import asciify_spaces, urlify_spaces
from lxml import html
import logging
import requests
import re


log = logging.getLogger('catalog')


def parse_code(code):
    '''
    Returns a tuple of the abbreviation and number from a course code.
    e.g. 'CS 1331' returns (CS, 1331)
    '''
    partition = code.partition(' ')
    return partition[0], int(partition[2])


def parse_hours(hours):
    '''
    Returns tuple of possible credit hours from a string.
    e.g. '1-3' appears fairly often, will return (1, 2, 3).
    '''
    nums = re.findall(r'[0-9]+', hours)
    if len(nums) > 1:
        lower_bound, upper_bound = int(nums[0]), int(nums[1])
        return tuple(range(lower_bound, upper_bound + 1))
    else:
        return (int(nums[0]))


def parse_title(title):
    '''
    Returns course code, course name, and credit hours from search result course block titles.
    e.g. 'CS 6475. Comp. Photography. 3 Credit Hours' returns (CS 6475, Comp. Photography, (3))
    '''
    code_per, hours_cut = title.find('.'), title.rfind('Credit Hour')
    code, title = asciify_spaces(title[:code_per]), title[code_per + 1:hours_cut].strip()
    last_per = title.rfind('.')
    name, hours = title[:last_per].strip(), parse_hours(title[last_per + 1:])
    return code, name, hours


def filter_by_degree(courses, degree):
    '''
    Applies a filter for a supported degree to a list of courses.
    i.e. only courses that can be taken by that degree are included.

    Preserves the original order of elements.
    '''
    results = []
    if degree not in supported_degrees:
        raise ValueError("{} degrees are not currently supported.".format(degree))
    for course in courses:
        code, range = int(re.search(r'[0-9]{4}', course)), degree_code_ranges[degree]
        if code >= range[0] and code <= range[1]:
            results.append(course)
    return results


def filter_by_abbr(courses, abbr):
    '''
    Given a list of courses and an abbreviation, e.g. CS, returns all
    courses in the list matching that abbreviation.
    '''
    return [course for course in courses if parse_code(course)[0] == abbr]


def lookup_course(code):
    '''
    Looks up a course using its course code.
    This makes use of catalog.gatech.edu's built-in search.

    e.g. 'CS 1331' returns ('CS 1331', 'Intro-Object Orient Prog', (3), <desc>)
    '''
    course = html.fromstring(requests.get(catalog_url + search_href + urlify_spaces(code))
        .content).xpath('//*[@id="fssearchresults"]/div[1]')
    if not len(course):
        raise ValueError("{} yielded no search results. It may not exist in the catalog.".format(code))
    block_title = course[0].xpath('.//h2/text()')[0]
    code, name, hours = parse_title(block_title)
    description = course[0].xpath('.//div/p/text()')[0].strip()
    return code, name, hours, description


def lookup_abbr(abbr, filter_abbr=None, filter_degree=None):
    '''
    Performs lookups based on known course code abbreviations.
    If passed in a degree, returns only the appropriate courses.

    Useful as requirements tables often use 'Any <abbr>' as shorthand.

    e.g. inputs ['HUM', 'SS', 'INTA']
    '''
    results = []
    if abbr not in unique_abbrs:
        search = html.fromstring(requests.get(catalog_url + courses_href + abbr.lower())
            .content).xpath('//*[@id="sc_sccoursedescs"]')[0]
        for course_block in search:
            results.append(parse_title(course_block[0].xpath('.//text()')[0])[0])
    else:
        table = html.fromstring(requests.get(catalog_url + unique_abbr_hrefs[abbr][0]).content).xpath(
            '//*[@id="textcontainer"]/table[' + str(unique_abbr_hrefs[abbr][1]) + ']')[0][3]
        for row in table:
            results.append(asciify_spaces(row[0][0].attrib['title']))
    results = sorted(list(set(results)))
    results = filter_by_abbr(results, filter_abbr) if filter_abbr else results
    results = filter_by_degree(results, filter_degree) if filter_degree else results
    return results


#print(lookup_course('MSE 3003'))
#print(lookup_abbr('CS'))
#print(lookup_abbr('HUM', filter_abbr='LMC'))