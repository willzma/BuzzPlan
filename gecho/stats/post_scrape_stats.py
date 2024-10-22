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
        print(program)
        for degree in catalog[program]:
            print(degree)
            if 'threads' in catalog[program][degree]:
                for thread in catalog[program][degree]['threads']:
                    print(thread)
                    requirements = catalog[program][degree]['threads'][thread]['requirements']
                    empty_count, invalid_count = 0, 0
                    for req in requirements:
                        if req['codes'] == []:
                            empty_count += 1
                        if req['hours'] == -1:
                            invalid_count += 1
                    if empty_count:
                        num_tables_with_empty_requirements += 1
                    if invalid_count:
                        num_tables_with_invalid_hours += 1
                    tables_with_errors.append((thread, empty_count, invalid_count))
            else:
                if 'requirements' in catalog[program][degree]:
                    requirements = catalog[program][degree]['requirements']['requirements']
                    empty_count, invalid_count = 0, 0
                    for req in requirements:
                        if req['codes'] == []:
                            empty_count += 1
                        if req['hours'] == -1:
                            invalid_count += 1
                    if empty_count:
                        num_tables_with_empty_requirements += 1
                    if invalid_count:
                        num_tables_with_invalid_hours += 1
                    tables_with_errors.append((degree + ' in ' + program, empty_count, invalid_count))
    print('{} tables had empty requirements.'.format(num_tables_with_empty_requirements))
    print('{} tables had invalid hours.'.format(num_tables_with_invalid_hours))
    with open ('post_scrape_stats.csv', 'w') as file:
        for course in tables_with_errors:
            print(course)
            file.write('{}, {}, {}, {}\n'.format(course[0].replace(u'\u200b', ' ').replace(',', ''), 
            course[1], 
            course[2], 
            course[1] + course[2]))