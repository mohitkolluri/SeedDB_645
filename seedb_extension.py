import database_connection
from sharing_optimization_extension import sharing_optimize
import constants
from pruning_optimization_extension import pruning_optimization



functions = ["sum","count", "max", "avg", "min"]
measures = ["age","capital_gain","capital_loss","hours_per_week","fnlwgt"]
aggregate= ["workclass","education","education_num","marital_status","occupation","relationship","race","sex",
"native_country","salary_range"]

def clear_db():
    for i in range(constants.PHASES):
        query_1 = f"drop table {constants.SCHEMA_NAME}.{constants.TABLE_NAME_MARRIED}_{i};"
        query_2 = f"drop table {constants.SCHEMA_NAME}.{constants.TABLE_NAME_UNMARRIED}_{i};"
        database_connection.execute_query(query_1)
        database_connection.execute_query(query_2)

    query = f"drop table {constants.SCHEMA_NAME}.{constants.TABLE_NAME}"
    database_connection.execute_query(query)


def test():
    total = 0
    print("test")
    for i in range(constants.PHASES):
        query_1 = f"select count(*) from {constants.SCHEMA_NAME}.{constants.TABLE_NAME_MARRIED}_{i};"
        query_2 = f"select count(*) from {constants.SCHEMA_NAME}.{constants.TABLE_NAME_UNMARRIED}_{i};"
        print(query_1)
        print(query_2)
        print("test",database_connection.execute_query(query_2)[0][0],database_connection.execute_query(query_1)[0][0])
        total+=database_connection.execute_query(query_1)[0][0]
        total+=database_connection.execute_query(query_2)[0][0]
    print(total)

def generate_fams():

    fam_set = set()

    for f in constants.functions:
        for m in constants.measures:
            i =0
            while i < len(constants.aggregates):
                j = i+1
                while j < len(constants.aggregates):
                    fam_set.add((f,constants.aggregates[i],constants.aggregates[j],m))
                    j += 1
                i += 1

    return fam_set

if __name__ == "__main__":

    clear_db()
    database_connection.setup_project()
    #test()

    #fam_set = {('min', 'education', 'capital_gain'), ('min', 'education', 'capital_loss'), ('min', 'education_num', 'capital_gain'), ('min', 'education_num', 'capital_loss'),('min', 'marital_status', 'capital_gain'), ('min', 'marital_status', 'capital_loss')}
    fam_set = generate_fams()
    #print(f"Length of fam_set = {len(fam_set)}")

    top_k_interesting_visualizations = pruning_optimization(fam_set)
    print(top_k_interesting_visualizations.keys())



