'''
Constants/variables used across catalog parsing modules.
'''

import logging
import sys


logger = logging.getLogger('gecho')
logger.setLevel(level=logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s - %(message)s'))
logger.addHandler(handler)

catalog_url = 'http://catalog.gatech.edu'
courses_href = '/coursesaz/'
search_href = '/search/?P='

# Core requirements (and corresponding abbreviations, potentially)
core_areas = {
    'Constitution and History': ('/academics/undergraduate/core-curriculum/constitution-history/', '//*[@id="textcontainer"]/div/table/tbody'),
    'A1': ('/academics/undergraduate/core-curriculum/core-area-a1/', '//*[@id="textcontainer"]/table/tbody'),
    'A2': ('/academics/undergraduate/core-curriculum/core-area-a2/', '//*[@id="textcontainer"]/table/tbody'),
    'B': ('/academics/undergraduate/core-curriculum/core-area-b/', '//*[@id="textcontainer"]/table[1]/tbody'),
    'C': ('/academics/undergraduate/core-curriculum/core-area-c/', '//*[@id="textcontainer"]/table[1]/tbody'),
    'D': ('/academics/undergraduate/core-curriculum/core-area-d/', '//*[@id="textcontainer"]/table[1]/tbody'),
    'E': ('/academics/undergraduate/core-curriculum/core-area-e/', '//*[@id="textcontainer"]/table[3]/tbody'),
    'Ethics': ('/academics/undergraduate/core-curriculum/ethics/', '//*[@id="textcontainer"]/div/table/tbody'),
    'Wellness': ('/academics/undergraduate/core-curriculum/wellness-requirement/', '//*[@id="textcontainer"]/table[1]/tbody')
}
unique_abbrs = {
    'HUM' : 'C',
    'SS' : 'E'
}

excluded_programs = ['Multidisciplinary Design/Arts History'] # Breaks database (can't contain '/' in key)

# Poorly formatted requirements tables, or with formats not yet supported
excluded_degrees = [
    'MS in Biomedical Engineering', # determined on an individual basis by student/advisors
    'MS in Building Construction and Facility Management' # lack of table structure
]

watchlist = [
    'Bachelor of Business Administration - Strategy and Innovation' # no consistency in table data
]

# Requirements tables are directly on the main page when linked (usually under a tab)
no_reqs_tabs = ['Mathematics']

supported_degrees = ['BS', 'MS']
degree_code_ranges = {'BS' : (1000, 4999), 'MS' : (6000, 9000)}

# Useful catalog numbers/statistics
class Statistics:
    num_programs = 0
    num_degrees = 0
    num_degrees_with_threads = 0
    num_degrees_with_no_requirements = 0
    num_threads = 0
    num_threads_with_no_requirements = 0
    num_rows = 0
    num_rows_with_no_course_codes = 0
    num_areaheaders = 0
    num_comments = 0
    num_unresolved_comments = 0
    num_courses = 0
    num_tables_with_errors = 0
    num_tables_with_unresolved_comments = 0