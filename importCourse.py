import json
import pprint
import argparse
import firebase_admin

from copy import deepcopy
from firebase_admin import credentials, db, firestore

def importData(filepath):
	print ("Start importing data from %s" % filepath)

	with open(filepath, 'r') as f:
		courses = json.load(f)


	course_offer = db.reference('Courses_2019_Spring')
	course_offer.delete()
	course_all = db.reference('Courses')
	course_all.delete()
	prerequisites = db.reference('Prerequisites')
	prerequisites.delete()

	pp = pprint.PrettyPrinter(indent=4)
	for c in courses:
		if course_all.child(c['identifier']).get():
			print ()
			print ('==================================')
			print ('Key duplicate in table Course and Prerequisites!!!!!')
			print ('==================================')
			print ()

		course_all.child(c['identifier']).set(c)

		if 'prerequisites' in c:
			prerequisites.child(c['identifier']).set(c['prerequisites'])

		if 'sections' not in c: 
			print ('%s: No section provides this sememster, skip.' % c['fullname'])
			continue
		
		sections = c.pop('sections')
		for s in sections:
			# if 'crn' not in s: print ('WARNING: \'crn\' not exists in section object, %s' % c['fullname'])
			# if 'instructors' not in s: print ('WARNING: \'instructor\' not exists in section object, %s' % c['fullname'])
			# if 'meetings' not in s: print ('WARNING: \'meetings\' not exists in section object, %s' % c['fullname'])
			# if 'section_id' not in s: print ('WARNING: \'section_id\' not exists in section object, %s' % c['fullname'])

			# if 'meetings' in s and len(s['meetings']) > 1:
			# 	print (s['meetings'])
			c.update(s)

			if course_offer.child(c['crn']).get():
				print ()
				print ('==================================')
				print ('Key duplicate in table Course and Prerequisites!!!!!')
				print ('==================================')
				print ()

			course_offer.child(c['crn']).set(c)
		
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('filepath', help="The path to the course data file")
	parser.add_argument('-c', '--crawl', action='store_true', help="If specified, crawl course data using Grouch Api and store to [filepath]")

	args = parser.parse_args()

	if args.crawl:
		print ('Crawl function has not been implement...')

	print ("Connecting to firebase database...")
	cred = credentials.Certificate('./credential.json')
	firebase_admin.initialize_app(cred, {'databaseURL': "https://buzzplan-d333f.firebaseio.com"})
	print ("Done")
	print ()

	importData(args.filepath)
