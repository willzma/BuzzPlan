from catalog import scrape_raw
from firebase_admin import credentials
from firebase_admin import db
import firebase_admin
import json


def scrape_firebase():
    cred = credentials.Certificate('buzzplan-d333f-firebase-adminsdk-jhebg-c6fbec263e.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://buzzplan-d333f.firebaseio.com/'
    })

    ref = db.reference()
    catalog_ref = ref.child('catalog')
    catalog_ref.set(scrape_raw())


if __name__ == "__main__":
    scrape_firebase()