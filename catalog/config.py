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

excluded_programs = ['Urban Design']

# Poorly formatted requirements tables, or with formats not yet supported
excluded_degrees = [
    'MS in Architecture', 
    'MS in Biomedical Engineering',
    'MS in Building Construction and Facility Management',
    'MS in Quantitative and Computational Finance',
    'MS in Statistics'
]

# Requirements tables are directly on the main page when linked (typically under a tab)
no_reqs_tabs = ['Mathematics']

supported_degrees = ['BS', 'MS']
degree_code_ranges = {'BS' : (1000, 4999), 'MS' : (6000, 9000)}

# Useful catalog numbers/statistics
num_programs = 0
num_degrees = 0
num_degrees_no_concentrations = 0