import json
import pprint

def check():
	with open('Grouch/result_all.json', 'r') as f:
		courses = json.load(f)

	pp = pprint.PrettyPrinter(indent=4)
	pre_map = {}
	for c in courses:
		if 'prerequisites' in c:
			pre_map[c['identifier']] = c['prerequisites']
			#pp.pprint(c['prerequisites'])
			#print('============================')

	for cls in pre_map.keys():
		if dfs(pre_map[cls], pre_map, pp):
			print ('This class is %s, and prerequisites is:' % cls)
			pp.pprint(pre_map[cls])
			print ('================================')

def dfs(pre, pre_map, pp):
	ret = False
	if type(pre) == type(str()):
		if pre in pre_map:
			print ('class %s need prerequisites:' % pre)
			pp.pprint(pre_map[pre])
			ret = True
	else:
		for obj in pre['courses']:
			ret |= dfs(obj, pre_map, pp)

	return ret


if __name__ == '__main__':
	check()