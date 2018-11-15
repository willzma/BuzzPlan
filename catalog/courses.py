'''
Functions for doing course lookups in the catalog.
'''

from config import catalog_url, courses_href, search_href, unique_abbrs, unique_abbr_hrefs
from config import supported_degrees, degree_code_ranges
from lxml import html
import requests
import re

def parse_hours(hours):
    '''
    Returns tuple of possible credit hours from a string.
    e.g. '1-3' appears fairly often, will return (1, 2, 3).
    '''
    if '-' in hours:
        hours = hours.partition('-')
        lower_bound, upper_bound = int(hours[0].strip()), int(hours[2].strip())
        return tuple(range(lower_bound, upper_bound + 1))
    else:
        return (int(hours))

def filter_by_degree(courses, degree):
    '''
    Applies a filter for a supported degree to a list of courses.
    i.e. only courses that can be taken by that degree are included.

    Preserves the original order of elements.
    '''
    results = []
    if degree not in supported_degrees:
        raise ValueError(degree + " degrees are not currently supported.")
    for course in courses:
        code, range = int(re.search(r'[0-9]{4}', course)), degree_code_ranges[degree]
        if code >= range[0] and code <= range[1]:
            results.append(course)
    return results

def lookup_course(code):
    '''
    Looks up a course using its course code.
    This makes use of catalog.gatech.edu's built-in search.

    e.g. 'CS 1331' returns ('CS 1331', 'Intro-Object Orient Prog', (3), <desc>)
    '''
    course = html.fromstring(requests.get(catalog_url + search_href + code.replace(' ', '%20'))
        .content).xpath('//*[@id="fssearchresults"]/div[1]')[0]
    course_info = course.xpath('.//h2/text()')[0].split('.')
    name, hours = course_info[1].strip(), parse_hours(course_info[2].partition('Credit Hour')[0].strip())
    description = course.xpath('.//div/p/text()')[0].strip()
    return code, name, hours, description

def lookup_abbrs(abbrs, degree=None):
    '''
    Performs lookups based on known course code abbreviations.
    If passed in a degree, returns only the appropriate courses.

    Useful as requirements tables often use 'Any <abbr>' as shorthand.

    e.g. ['HUM', 'SS', 'INTA']
    '''
    results = []
    for abbr in abbrs: # This needs to be replaced with a regex solution... see CS 6475 example
        if abbr not in unique_abbrs:
            search = html.fromstring(requests.get(catalog_url + courses_href + abbr.lower())
                .content).xpath('//*[@id="sc_sccoursedescs"]')[0]
            for course_block in search:
                title = course_block[0].xpath('.//text()')[0].split('.')
                title = list(filter(None, title))
                code, name = title[0].strip().replace(u'\xa0', ' '), title[1].strip()
                hours = parse_hours(title[2].partition('Credit Hour')[0].strip())
                results.append((code, name, hours))
        else:
            table = html.fromstring(requests.get(catalog_url + unique_abbr_hrefs[abbr][0]).content).xpath(
                '//*[@id="textcontainer"]/table[' + str(unique_abbr_hrefs[abbr][1]) + ']')[0][3]
            for row in table:
                code = row[0][0].attrib['title'].replace(u'\xa0', ' ')
                name, hours = row[1].xpath('.//text()')[0], parse_hours(row[2].xpath('.//text()')[0])
                results.append((code, name, hours))
    results = sorted(list(set(results)))
    return filter_by_degree(results, degree) if degree else results

print(lookup_abbrs(['CS']))