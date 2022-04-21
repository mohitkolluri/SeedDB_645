import psycopg2
import constants
'''
INSTRUCTIONS FOR SETTING UP DB: 
Download postgres: 
Windows: https://www.postgresql.org/download/windows/
Macbook: https://wiki.postgresql.org/wiki/Homebrew
---------------------------------------
Enter postgres CLI using 'psql postgres'

--> CREATE DATABASE seeddb
--> create user team_645_seeddb
--> ALTER USER team_645_seeddb WITH SUPERUSER;
------------------------------------------
Place adult.data in this directory downloaded from 
https://archive.ics.uci.edu/ml/machine-learning-databases/adult/

-------------------------------------------
--> Run 'pip install -r requirements.txt'

--> Run 'python3 database_connection.py'

-----------------------------------------------------------------
EXECUTING QUERIES FROM THE DB

Import this module and use the function 'execute_query(query)' of this file
'''

HOST = "127.0.0.1"
PORT = '5432'
DATABASE = 'seeddb'
USER = 'team_645_seeddb'


COLUMNS_DICT = {'age':'INTEGER', 
'workclass': 'VARCHAR', 'fnlwgt': 'INTEGER',
'education': 'VARCHAR', 'education_num': 'INTEGER', 'marital_status': 'VARCHAR',
'occupation':'VARCHAR', 'relationship': 'VARCHAR',
'race': 'VARCHAR', 'sex': 'VARCHAR', 
'capital_gain': 'INTEGER', 'capital_loss': 'INTEGER',
'hours_per_week': 'INTEGER', 'native_country': 'VARCHAR', 'salary_range': 'VARCHAR'}


def read_file(filename='adult.data'):
    data_type = list(COLUMNS_DICT.values())
    rows = []
    with open(filename, 'r') as f:
        counter = 0
        for line in f.readlines():


            print(line)
            row = []
            line_list = line.split(',')
            if len(line_list) != len(data_type):
                continue
            for i in range(len(COLUMNS_DICT)):

                if data_type[i] == 'INTEGER':
                    row.append(line_list[i].strip())

                else:
                    row.append("'"+line_list[i].strip()+"'")

            row = '(' + ','.join(row) + ')'
            rows.append(row)

    return rows

def connect_database():

    conn = psycopg2.connect(
    host=HOST,
    port=PORT,
    database=DATABASE,
    user=USER,
    password="1234")

    return conn

def execute_query(query):
    connection = connect_database()
    cur = connection.cursor()
    #print(query)
    try:
        cur.execute(query)
        result = cur.fetchall()
    except Exception as e:
        print(e)
        result = None
    cur.close()
    connection.commit()
    connection.close()
    return result


def create_schema(schema_name):
    query = f'CREATE SCHEMA IF NOT EXISTS {schema_name};'
    return execute_query(query)

def create_table(table_name, schema_name, columns_dict):
    columns = []
    for column, data_type in columns_dict.items():
        columns.append(f'{column} {data_type}')
    columns = ','.join(columns)
    for i in range(constants.PHASES):
        query = f'CREATE TABLE IF NOT EXISTS {schema_name}.{table_name}_{i} ({columns});'
        try:
            execute_query(query)
            result = "Success"
        except Exception as e:
            print(e)
            result = None
    return result

def create_main_table(table_name, schema_name, columns_dict):
    columns = []
    for column, data_type in columns_dict.items():
        columns.append(f'{column} {data_type}')
    columns = ','.join(columns)

    query = f'CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} ({columns});'
    try:
        execute_query(query)
        result = "Success"
    except Exception as e:
        print(e)
        result = None
    return result

def split_data(curr_list):
    married=[]
    unmarried = []
    married_matches=["Married","Seperated"]
    for row in curr_list:
        if any(x in row for x in married_matches):
            married.append(row)
        else:
            unmarried.append(row)
    return married, unmarried

def insert_to_table(schema_name, rows_list):
    number_of_records= len(rows_list)
    split, r = divmod(number_of_records,constants.PHASES)
    for i in range(constants.PHASES):
        if i==constants.PHASES-1:
            curr_list=rows_list[i*split:]
        else:
            curr_list=rows_list[i*split:i*split+split]
        married,unmarried = split_data(curr_list)
        query_married = f"insert into {schema_name}.{constants.TABLE_NAME_MARRIED}_{i} values {','.join(married)}"
        query_unmarried = f"insert into {schema_name}.{constants.TABLE_NAME_UNMARRIED}_{i} values {','.join(unmarried)}"
        
        try:
            execute_query(query_married)
            execute_query(query_unmarried)
            result = "Success"
        except Exception as e:
            print(e)
            result = None

    #print(f"insert into {schema_name}.{constants.TABLE_NAME}")
    query_main_table = f"insert into {schema_name}.{constants.TABLE_NAME} values {','.join(rows_list)}"
    execute_query(query_main_table)
    return result


def setup_project():
    print(create_schema(constants.SCHEMA_NAME))
    print(create_table(constants.TABLE_NAME_MARRIED, constants.SCHEMA_NAME, COLUMNS_DICT))
    print(create_table(constants.TABLE_NAME_UNMARRIED, constants.SCHEMA_NAME, COLUMNS_DICT))
    print(create_main_table(constants.TABLE_NAME, constants.SCHEMA_NAME, COLUMNS_DICT))
    rows_list = read_file()
    print(len(rows_list))
    print(insert_to_table(constants.SCHEMA_NAME, rows_list))

if __name__ == "__main__":
    setup_project()




