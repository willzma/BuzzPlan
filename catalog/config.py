'''
Constants/variables used across catalog parsing modules.
'''

import logging
import sys


logger = logging.getLogger('catalog')
logger.setLevel(level=logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s - %(message)s'))
logger.addHandler(handler)

catalog_url = 'http://catalog.gatech.edu'
courses_href = '/coursesaz/'
search_href = '/search/?P='

unique_abbrs = ['HUM', 'SS']
unique_abbr_hrefs = {
    'HUM' : ('/academics/undergraduate/core-curriculum/core-area-c/', 1),
    'SS' : ('/academics/undergraduate/core-curriculum/core-area-e/', 3)
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

# Requirements tables are directly on the main page when linked (typically under a tab)
no_reqs_tabs = ['Mathematics']

supported_degrees = ['BS', 'MS']
degree_code_ranges = {'BS' : (1000, 4999), 'MS' : (6000, 9000)}

# Useful catalog numbers/statistics
num_programs = 0
num_degrees = 0
num_degrees_with_threads = 0
num_threads = 0