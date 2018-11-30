import json
import pprint
import argparse
import firebase_admin

import numpy as np

from copy import deepcopy
from firebase_admin import credentials, db, firestore

pp = pprint.PrettyPrinter(indent=4)

def valid_identifier(identifier):
	splited = identifier.split(' ')

	if len(splited) != 2 or not splited[0].isupper() or not splited[1].isdigit():
		return False

	return True

def is_X(identifier):
	splited = identifier.split(' ')

	if len(splited) != 2:
		return False

	num = splited[1]
	idx = num.find('X')
	while idx != -1:
		num = num[:idx] + num[idx + 1:]
		idx = num.find('X')

	if num.isdigit(): return True
	else: return False

def count_graph_size(cur, prerequisites, encounter_cls, counts, start=False):
	if type(cur) == type(str()):
		if cur in encounter_cls:
			return 

		encounter_cls.add(cur)
		counts[0] += 1
		if cur in prerequisites:
			count_graph_size(prerequisites[cur], prerequisites, encounter_cls, counts, start=True)

	else:
		if not start: counts[0] += 1

		for obj in cur['courses']:
			counts[1] += 1
			count_graph_size(obj, prerequisites, encounter_cls, counts, start=False)

def get_level(pre):
	level = 1
	for element in pre['courses']:
		if type(element) == type({}):
			level = max(level, 1 + get_level(element))

	return level

def prune(pre, threshold, level=0):

	if level >= threshold:
		i = 0
		while i < len(pre['courses']):
			if type(pre['courses'][i]) == type({}):
				print ('prune')
				del pre['courses'][i]
			else: i += 1
	else:
		for element in pre['courses']:
			if type(element) == type({}):
					prune(element, threshold, level=level + 1)

def dfs_process_prerequisite(pre, invalid_list, id_set, counts):
	if 'courses' not in pre or 'type' not in pre:
		print ('invalid structure')
		return None, 1

	pre_list = pre['courses']
	pre_type = pre['type']

	process_list = []


	for element in pre_list:
		if type(element) == type(str()):
			if valid_identifier(element):
				process_list.append(element)
				if element not in id_set:
					print (element)
					counts[1] += 1
			else:
				if is_X(element): invalid_list[0].append(element)
				else: invalid_list[1].append(element)

			counts[0] += 1

		elif type(element) == type({}):
			obj = dfs_process_prerequisite(element, invalid_list, id_set, counts)
			if not obj: continue

			if pre_type == obj['type'] or len(obj['courses']) == 1:
				process_list.extend(obj['courses'])

			process_list.append(obj)
		else:
			print ('WARNING: unexpect data structure in first level: %s' % type(element))

	if len(process_list) == 0:
		return None

	if len(process_list) == 1 and type(process_list[0]) == type({}):
		return process_list[0]

	obj = {	'courses': process_list,
			'type': pre_type}

	return obj


def process_prerequisite(pre):
	if 'courses' not in pre or 'type' not in pre:
		return None

	pre_list = pre['courses']
	pre_type = pre['type']

	process_list = []

	invalid = []
	element_count = 0

	for element in pre_list:
		if type(element) == type(str()):
			if valid_identifier(element):
				process_list.append(element)
			else:
				invalid.append(element)

			element_count += 1

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

def updatePrerequisite(filepath, update=False):
	print ("Start updating prerequisites from %s" % filepath)

	with open(filepath, 'r') as f:
		courses = json.load(f)

	if update:
		prerequisites = db.reference('Prerequisites')
		prerequisites.delete()	
	raw_pre = {}
	processed_pre = {}
	prune_pre = {}
	invalid_list = [[], []]
	pre_count = 0
	counts = [0, 0]

	id_set = set()
	for c in courses:
		id_set.add(c['identifier'])

	for c in courses:
		if 'prerequisites' in c:
			pre_count += 1
			raw_pre[c['identifier']] = c['prerequisites']
			#processed = process_prerequisite(c['prerequisites'])
			processed = dfs_process_prerequisite(c['prerequisites'], invalid_list, id_set, counts)
			if not processed:
				continue

			processed_pre[c['identifier']] = processed
			processed_copy = deepcopy(processed)
			prune(processed, 1)

			prune_pre[c['identifier']] = processed_copy

			if update:
				prerequisites.child(c['identifier']).set(processed)


	size_diffs = []
	biggest_raw, biggest_raw_cls, biggest_prune, biggest_prune_cls = 0, '', 0, ''
	for cls in raw_pre.keys():
		raw_counts = [0, 0]
		count_graph_size(cls, raw_pre, set(), raw_counts)
		raw_size = raw_counts[0] + raw_counts[1]

		if raw_size > biggest_raw:
			biggest_raw = raw_size
			biggest_raw_cls = cls

		processed_counts = [0, 0]
		if cls in processed_pre:
			count_graph_size(cls, processed_pre, set(), processed_counts)
		processed_size = processed_counts[0] + processed_counts[1]

		size_diffs.append((raw_size - processed_size) / raw_size)

		prune_counts = [0, 0]
		if cls in prune_pre:
			count_graph_size(cls, prune_pre, set(), prune_counts)
		prune_size = prune_counts[0] + prune_counts[1]

		if prune_size > biggest_prune:
			biggest_prune = prune_size
			biggest_prune_cls = cls





	element_count, element_not_in_id = counts[0], counts[1]
	#print (invalid_list[0])
	#print (invalid_list[1])
	print ('Number of course need prerequisites: %d' % pre_count)
	print ('Number of element: %d' % element_count)
	print ('Number of invalid element: %d' % len(invalid_list[1]))
	print ('Number of identifier with "X": %d' % len(invalid_list[0]))
	print ('Number of element not in id: %d' % element_not_in_id)

	print ('Biggest Raw Graph: %s, %d' % (biggest_raw_cls, biggest_raw))
	print ('Biggest Prune Graph: %s, %d' % (biggest_prune_cls, biggest_prune))
	print (size_diffs[19])
	print ('Reduce Amount: %f (%f)' % (np.mean(size_diffs), np.std(size_diffs)))
	#print (len(invalid_list) / element_count)

	pre_map = create_map(processed_pre)

	if update:
		prerequisite_map = db.reference('prerequisite_map')
		prerequisite_map.set(pre_map)


def create_map(prerequisites):
	pre_map = {}
	counts = {}
	cycle_count = 0
	for cls in prerequisites.keys():
		encounter_cls = set()
		#print ('Processing prerequisite map for %s' % cls)
		counts[cls] = dfs(cls, prerequisites, encounter_cls, set()) 
		if counts[cls] > 0:
			cycle_count += 1

		pre_map[cls] = list(encounter_cls)

	print ('Percentages of Cycle: %f' % (cycle_count / len(counts)))
	return pre_map		

def dfs(cur, prerequisites, encounter_cls, path):
	#print (cur)
	count = 0
	if type(cur) == type(str()):
		if cur in prerequisites:
			if cur in path:
				#print ("WARNING: Cycle detected...")
				return 1

			if cur in encounter_cls:
				return count 

			encounter_cls.add(cur)
			path.add(cur)
			count += dfs(prerequisites[cur], prerequisites, encounter_cls, path)
			path.remove(cur)

	else:
		for obj in cur['courses']:
			count += dfs(obj, prerequisites, encounter_cls, path)

	return count

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('filepath', help="The path to the course data file")
	parser.add_argument('-u', '--update', action='store_true', help="If specified, update prerequisites in database")

	args = parser.parse_args()

	if args.update:
		print ("Connecting to firebase database...")
		cred = credentials.Certificate('./credential.json')
		firebase_admin.initialize_app(cred, {'databaseURL': "https://buzzplan-d333f.firebaseio.com"})
		print ("Done")
		print ()


	updatePrerequisite(args.filepath)
	#print (count_graph_size(pre))