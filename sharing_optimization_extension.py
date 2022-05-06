import constants
from database_connection import execute_query
'''
Developed by:
Priyanshi Somani
psomani@umass.edu
'''
def sharing_optimize(queries,phase):
	aggregate_map = {}
	result_dict_married = {}
	result_dict_unmarried = {}
	for (f,a1,a2,m) in queries:
		if (a1,a2) in aggregate_map:
			aggregate_map[(a1,a2)][0] += f',{f}({m})'
			aggregate_map[(a1,a2)][1].append((f,a1,a2,m))
		else:
			aggregate_map[(a1,a2)] = ['', []]
			aggregate_map[(a1,a2)][0] = f',{f}({m})'
			aggregate_map[(a1,a2)][1].append((f,a1,a2,m))
	queries_to_execute = {"married":[],"unmarried":[]}
	for (a1,a2),row in aggregate_map.items():
		q, fams = row[0], row[1]
		#f,a,m = fam
		query_married = f'select {a1},{a2}{q} from {constants.SCHEMA_NAME}.{constants.TABLE_NAME_MARRIED}_{phase} GROUP BY {a1},{a2};'
		query_unmarried = f'select {a1},{a2}{q} from {constants.SCHEMA_NAME}.{constants.TABLE_NAME_UNMARRIED}_{phase} GROUP BY {a1},{a2};'
		#print(query_married)
		

		
		for status in ["married","unmarried"]:
			query = 'query_'+ status
			result = execute_query(eval(query))
			# if a == 'sex':
			# 	print(result)
			for row in result:
				agg_val = (row[0],row[1])
				for i in range(len(fams)):
					f,a1,a2,m = fams[i]
					fam = fams[i]
					fm_val = row[i+2]

					
					if status == "married":
						if fam not in result_dict_married:
							result_dict_married[fam] = {}
						result_dict_married[fam][agg_val] = fm_val
					else:
						if fam not in result_dict_unmarried:
							result_dict_unmarried[fam] = {}
						result_dict_unmarried[fam][agg_val] = fm_val

	return result_dict_married,result_dict_unmarried











