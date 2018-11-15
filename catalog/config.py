'''
Constants/variables used across catalog parsing modules.
'''

catalog_url = 'http://catalog.gatech.edu'
courses_href = '/coursesaz/'
search_href = '/search/?P='

unique_abbrs = ['HUM', 'SS']
unique_abbr_hrefs = {'HUM' : ('/academics/undergraduate/core-curriculum/core-area-c/', 1), 
                     'SS' : ('/academics/undergraduate/core-curriculum/core-area-e/', 3)
                    }

excluded_programs = ['Urban Design']

supported_degrees = ['BS', 'MS']
degree_code_ranges = {'BS' : (1000, 4999), 'MS' : (6000, 9000)}

# Useful catalog numbers/statistics
num_programs = 0
num_degrees = 0
num_degrees_no_concentrations = 0