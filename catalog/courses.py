'''
Functions for doing course lookups in the catalog.
'''

from config import catalog_url, courses_href, search_href, unique_abbrs
from config import core_areas, supported_degrees, degree_code_ranges
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
    return partition[0], int(re.findall(r'[0-9]{4}', partition[2])[0])


def parse_formatted_table(table):
    '''
    Assuming a well-formatted table with uniform structure (unlike requirements.py),
    returns a list of course codes as parsed from the table.
    '''
    return [asciify_spaces(row[0][0].attrib['title']) for row in table]


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
        code, range = int(re.findall(r'[0-9]{4}', course)[0]), degree_code_ranges[degree]
        if code >= range[0] and code <= range[1]:
            results.append(course)
    return results


def filter_by_abbr(courses, abbr):
    '''
    Given a list of courses and an abbreviation, e.g. CS, returns all
    courses in the list matching that abbreviation.
    '''
    return [c for c in courses if parse_code(c)[0] == abbr]


def filter_by_range(courses, start=1000, end=9999):
    '''
    Given a list of courses and an abbreviation, e.g. CS, returns all
    courses with codes greater than start, and less than end.
    '''
    return [c for c in courses if parse_code(c)[1] >= start and parse_code(c)[1] <= end]


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


def lookup_abbr(abbr, filter_abbr=None, filter_degree=None, start=1000, end=9999):
    '''
    Performs lookups based on known course code abbreviations.
    If passed in a degree, returns only the appropriate courses.

    Useful as requirements tables often use 'Any <abbr>' as shorthand.

    e.g. inputs ['HUM', 'SS', 'INTA']
    '''
    results = []
    if abbr not in unique_abbrs.keys():
        search = html.fromstring(requests.get(catalog_url + courses_href + abbr.lower())
            .content).xpath('//*[@id="sc_sccoursedescs"]')[0]
        for course_block in search:
            result = parse_title(course_block[0].xpath('.//text()')[0])[0]
            if re.findall(r'[0-9]{4}', result): # Filter out results with X's in their codes
                results.append(result)
    else:
        results = get_core_area(unique_abbrs[abbr])
    results = filter_by_abbr(results, filter_abbr) if filter_abbr else results
    results = filter_by_range(results, start, end) if start or end else results
    results = filter_by_degree(results, filter_degree) if filter_degree else results
    return results


def get_core_area(area):
    if area not in core_areas.keys():
        raise ValueError('Core area {} doesn\'t exist'.format(area))
    table = html.fromstring(requests.get(catalog_url + core_areas[area][0]).content).xpath(core_areas[area][1])[0]
    return parse_formatted_table(table)


#print(lookup_course('MSE 3003'))
#print(lookup_abbr('CS'))
#print(lookup_abbr('HUM', filter_abbr='LMC'))
#print(lookup_abbr('FREN', start=3000, end=4999))
#print(get_core_area('Constitution and History'))