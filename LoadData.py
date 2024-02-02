import pandas as pd
import sys 
import pyodbc 
from dotenv import load_dotenv
import os

load_dotenv
# SQL Server Configuration
driver = "{ODBC Driver 18 for SQL Server}"
username = os.getenv('SQL_USERNAME')
server = f"tcp:{os.getenv('SQL_ENDPOINT')}"
password = os.getenv('SQL_PASSWORD')
database = os.getenv('SQL_DATABASE')

def create_table(table_name, df):
    # df = pd.read_csv(path).fillna(value=0)
    # file = df.drop(df.iloc[:, 10:], axis =1)

    head = df.columns
    types = df.dtypes
    table = [f"{head} {types[head]}" for head in head]
    list = [item.replace("64", "").replace("object", "varchar(200)") for item in table]
    query = f"""
    CREATE TABLE {table_name} (
        {" NOT NULL, ".join(list)} NOT NULL
    );
    """
    return query

def insert_query(table_name, df, row):  
    columns = df.columns.tolist()  
    placeholders = ','.join(['?'] * len(columns))  
    column_names = ', '.join(columns)  
    values = tuple(row[col] for col in columns)  
    sql_insert_statement = f"INSERT INTO {table_name} ({column_names}) values({placeholders})"  
    return sql_insert_statement, values 

file = pd.read_csv(sys.argv[1]).fillna(value=0)

con = pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}')  
cursor = con.cursor()

cursor.execute(create_table("LIVRES2", file))

for index, row in file.iterrows():
    sql_query, values = insert_query("LIVRES2", file, row)
    cursor.execute(sql_query, values)

con.commit()
cursor.close()


# con = pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}')  
# cursor = con.cursor()
# print(cursor.execute("SELECT * FROM dbo.[Titanic]"))
# results = cursor.fetchall()

# for row in results:
#     print(row)