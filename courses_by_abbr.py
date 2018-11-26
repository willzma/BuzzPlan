from gecho.courses import lookup_course
from firebase_admin import credentials
from firebase_admin import db
import firebase_admin
import json

if __name__ == '__main__':
    cred = credentials.Certificate('buzzplan-d333f-firebase-adminsdk-jhebg-c6fbec263e.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://buzzplan-d333f.firebaseio.com/'
    })
    ref = db.reference()
    courses_ref = ref.child('Courses')
    courses_by_abbr_ref = ref.child('courses_by_abbr')
    courses = courses_ref.get()
    courses_by_abbr_dict = {}
    for key in courses:
        cutoff_index = None
        for i in range(len(key)):
            if key[i].isnumeric():
                cutoff_index = i
                break
        abbr = key[:cutoff_index - 1].strip()
        code = key[cutoff_index:].strip()
        if abbr not in courses_by_abbr_dict:
            courses_by_abbr_dict[abbr] = {}
        if 'X' not in code:
            courses_by_abbr_dict[abbr][key] = courses[key]
            try:
                description = lookup_course(key)[3]
                courses_by_abbr_dict[abbr][key]['description'] = description
            except:
                print(key)
    courses_by_abbr_ref.set(courses_by_abbr_dict)