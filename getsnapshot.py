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
    with open('db.json', 'w') as f:
        json.dump(ref.get(), f)