from firebase_admin import credentials
from firebase_admin import db
import firebase_admin
import json
import sys

sys.path.append('../')
from courses import lookup_course

if __name__ == '__main__':
    total_courses_in_oscar = 0
    total_courses_not_found = 0
    total_improperly_formatted = 0

    cred = credentials.Certificate('../buzzplan-d333f-firebase-adminsdk-jhebg-c6fbec263e.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://buzzplan-d333f.firebaseio.com/'
    })
    ref = db.reference()
    courses_ref = ref.child('Courses')
    courses = courses_ref.get()
    courses_not_found = []
    for key in courses:
        cutoff_index = None
        for i in range(len(key)):
            if key[i].isnumeric():
                cutoff_index = i
                break
        abbr = key[:cutoff_index - 1].strip()
        code = key[cutoff_index:].strip()
        if 'X' not in code:
            print('Looking up course {}... '.format(key), end='')
            try:
                description = lookup_course(key)[3]
            except:
                print('Failed.', end='')
                total_courses_not_found += 1
                courses_not_found.append(key)
            total_courses_in_oscar += 1
        else:
            total_improperly_formatted += 1
        print('')
    with open ('catalog_vs_oscar.txt', 'w') as file:
        file.write('{} out of {} courses were not found in the catalog.\n'.format(
            total_courses_not_found, total_courses_in_oscar))
        file.write('{} stored courses had improperly formatted names.\n'.format(total_improperly_formatted))
        file.write('The courses not found will be listed below:\n')
        for course in courses_not_found:
            file.write('{}\n'.format(course))