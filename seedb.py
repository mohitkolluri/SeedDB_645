import database_connection
TABLE_NAME_MARRIED = 'adult_married'
TABLE_NAME_UNMARRIED = 'adult_unmarried'
SCHEMA_NAME = 'census_income'
PHASES = 10

def clear_db():
    for i in range(PHASES):
        query_1 = f"drop table {SCHEMA_NAME}.{TABLE_NAME_MARRIED}_{i};"
        query_2 = f"drop table {SCHEMA_NAME}.{TABLE_NAME_UNMARRIED}_{i};"
        database_connection.execute_query(query_1)
        database_connection.execute_query(query_2)

def test():
    total = 0
    print("test")
    for i in range(PHASES):
        query_1 = f"select count(*) from {SCHEMA_NAME}.{TABLE_NAME_MARRIED}_{i};"
        query_2 = f"select count(*) from {SCHEMA_NAME}.{TABLE_NAME_UNMARRIED}_{i};"
        print(query_1)
        print(query_2)
        print("test",database_connection.execute_query(query_2)[0][0],database_connection.execute_query(query_1)[0][0])
        total+=database_connection.execute_query(query_1)[0][0]
        total+=database_connection.execute_query(query_2)[0][0]
    print(total)




if __name__ == "__main__":
    clear_db()
    database_connection.setup_project()
    test()

