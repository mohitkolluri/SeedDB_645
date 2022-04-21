import constants
from database_connection import execute_query

def sharing_optimize(queries,phase):
	aggregate_map = {}
	result_dict_married = {}
	result_dict_unmarried = {}
	for (f,a,m) in queries:
		if a in aggregate_map:
			aggregate_map[a][0] += f',{f}({m})'
			aggregate_map[a][1].append((f,a,m))
		else:
			aggregate_map[a] = ['', []]
			aggregate_map[a][0] = f',{f}({m})'
			aggregate_map[a][1].append((f,a,m))
	queries_to_execute = {"married":[],"unmarried":[]}
	for a,row in aggregate_map.items():
		q, fams = row[0], row[1]
		#f,a,m = fam
		query_married = f'select {a}{q} from {constants.SCHEMA_NAME}.{constants.TABLE_NAME_MARRIED}_{phase} GROUP BY {a};'
		query_unmarried = f'select {a}{q} from {constants.SCHEMA_NAME}.{constants.TABLE_NAME_UNMARRIED}_{phase} GROUP BY {a};'
		print(query_married)
		

		
		for status in ["married","unmarried"]:
			query = 'query_'+ status
			result = execute_query(eval(query))
			# if a == 'sex':
			# 	print(result)
			for row in result:
				agg_val = row[0]
				for i in range(len(fams)):
					f,a,m = fams[i]
					fam = fams[i]
					fm_val = row[i+1]

					
					if status == "married":
						if fam not in result_dict_married:
							result_dict_married[fam] = {}
						result_dict_married[fam][agg_val] = fm_val
					else:
						if fam not in result_dict_unmarried:
							result_dict_unmarried[fam] = {}
						result_dict_unmarried[fam][agg_val] = fm_val

	#print(result_dict_married[('avg', 'sex', 'capital_gain')])
	return result_dict_married,result_dict_unmarried











