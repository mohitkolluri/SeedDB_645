import psycopg2
'''
INSTRUCTIONS FOR SETTING UP DB: 
Download postgres: 
Windows: https://www.postgresql.org/download/windows/
Macbook: https://wiki.postgresql.org/wiki/Homebrew
---------------------------------------
Enter postgres CLI using 'psql postgres'

--> CREATE DATABASE SeedDB
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

SCHEMA_NAME = 'census_income'
TABLE_NAME = 'adult'
COLUMNS_DICT = {'age':'INTEGER', 
'workclass': 'VARCHAR', 'fnlwgt': 'INTEGER',
'education': 'VARCHAR', 'education_num': 'INTEGER', 'marital_status': 'VARCHAR',
'occupation':'VARCHAR', 'relationshiop': 'VARCHAR',
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
    user=USER)

    return conn

def execute_query(query):
    connection = connect_database()
    cur = connection.cursor()
    print(query)
    cur.execute(query)
    try:
        result = cur.fetchall()
    except:
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
    query = f'CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} ({columns});'
    return execute_query(query)

    print(query)

def insert_to_table(table_name, schema_name, rows_list):

    query = f"insert into {schema_name}.{table_name} values {','.join(rows_list)}"
    return execute_query(query)

def setup_project():
    print(create_schema(SCHEMA_NAME))
    print(create_table(TABLE_NAME, SCHEMA_NAME, COLUMNS_DICT))
    rows_list = read_file()
    print(insert_to_table(TABLE_NAME, SCHEMA_NAME, rows_list))

if __name__ == "__main__":
    setup_project()




