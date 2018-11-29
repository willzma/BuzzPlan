from firebase_admin import credentials
from firebase_admin import db
import firebase_admin
import json
import sys

sys.path.append('../')
from catalog import scrape_raw

if __name__ == '__main__':
    num_tables_with_empty_requirements = 0
    num_tables_with_invalid_hours = 0
    tables_with_errors = []
    catalog = scrape_raw()
    for program in catalog:
        for degree in program:
            if 'threads' in degree:
                for thread in degree['threads']:
                    requirements = thread['requirements']
                    empty_count, invalid_count = 0, 0
                    for req in requirements:
                        if req.codes == []:
                            num_tables_with_empty_requirements += 1
                            empty_count += 1
                        if req.hours == -1:
                            num_tables_with_invalid_hours += 1
                            invalid_count += 1
                    tables_with_errors.append((thread, empty_count, invalid_count))
            else:
                requirements = degree['requirements']
                empty_count, invalid_count = 0, 0
                for req in requirements:
                    if req.codes == []:
                        num_tables_with_empty_requirements += 1
                        empty_count += 1
                    if req.hours == -1:
                        num_tables_with_invalid_hours += 1
                        invalid_count += 1
                tables_with_errors.append((thread, empty_count, invalid_count))
    print('{} tables had empty requirements.'.format(num_tables_with_empty_requirements))
    print('{} tables had invalid hours.'.format(num_tables_with_invalid_hours))
    with open ('post_scrape_stats.csv', 'w') as file:
        for course in tables_with_errors:
            file.write('{}, {}, {}, {}'.format(course[0], course[1], course[2], course[2] + course[3]))