import json
import pprint
import argparse
import firebase_admin

from copy import deepcopy
from firebase_admin import credentials, db, firestore

pp = pprint.PrettyPrinter(indent=4)

def valid_identifier(identifier):
	splited = identifier.split(' ')

	if len(splited) != 2 or not splited[0].isupper() or not splited[1].isdigit():
		return False

	return True

def add_description():
	course_offer = db.reference('Courses_2019_Spring').get()

	for c in course_offer.keys():
		description = db.reference('courses_by_abbr').child(course_offer[c]['school']).child(course_offer[c]['identifier']).child('description').get()
		if not description:
			description = ''

		print(description)
		db.reference('Courses_2019_Spring').child(c).child('description').set(description)


def process_prerequisite(pre):
	if 'courses' not in pre or 'type' not in pre:
		return None

	pre_list = pre['courses']
	pre_type = pre['type']

	process_list = []

	for element in pre_list:
		if type(element) == type(str()):
			if valid_identifier(element):
				process_list.append(element)

		elif type(element) == type({}):
			if 'courses' not in element or 'type' not in element:
				continue

			nest_list = element['courses']
			nest_type = element['type']
			nest_process_list = []

			for nest_element in nest_list:
				if type(nest_element) != type(str()):
					print ('WARNING: unexpect data structure in second level: %s' % type(nest_element))
					pp.pprint(pre)
					continue

				if valid_identifier(nest_element):
					nest_process_list.append(nest_element)

			if len(nest_process_list) == 0:
				continue

			if nest_type == pre_type or len(nest_process_list) == 1:
				print ('Merge second level object to first level.')
				process_list.extend(nest_process_list)
				continue

			process_list.append({'courses': nest_process_list,
								 'type': nest_type})

		else:
			print ('WARNING: unexpect data structure in first level: %s' % type(element))



	if len(process_list) == 0:
		return None

	if len(process_list) == 1 and type(process_list[0]) == type({}):
		return process_list[0]

	return {'courses': process_list,
			'type': pre_type}

def updatePrerequisite(filepath):
	print ("Start updating prerequisites from %s" % filepath)

	with open(filepath, 'r') as f:
		courses = json.load(f)

	prerequisites = db.reference('Prerequisites')
	#prerequisites.delete()	

	processed_pre = {}
	for c in courses:
		if 'prerequisites' in c:
			processed = process_prerequisite(c['prerequisites'])
			if not processed:
				continue

			processed_pre[c['identifier']] = processed

			#prerequisites.child(c['identifier']).set(processed)

	prerequisite_map = db.reference('prerequisite_map')
	pre_map = create_map(processed_pre)

	print (pre_map['MATH 4320'])
	print (processed_pre['MATH 1111'])
	prerequisite_map.set(pre_map)


def create_map(prerequisites):
	pre_map = {}
	for cls in prerequisites.keys():
		encounter_cls = set()
		print ('Processing prerequisite map for %s' % cls)
		dfs(cls, prerequisites, encounter_cls)
		pre_map[cls] = list(encounter_cls)

	return pre_map
			

def dfs(cur, prerequisites, encounter_cls):
	#print (cur)
	if type(cur) == type(str()):
		if cur in prerequisites:
			if cur in encounter_cls:
				print ("WARNING: Cycle detected...")
				return 
			encounter_cls.add(cur)
			dfs(prerequisites[cur], prerequisites, encounter_cls)

	else:
		for obj in cur['courses']:
			dfs(obj, prerequisites, encounter_cls)





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

	#importData(args.filepath)
	#updatePrerequisite(args.filepath)
	add_description()
	


