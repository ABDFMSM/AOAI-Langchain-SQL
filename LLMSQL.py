from sqlalchemy import create_engine, engine
from langchain.sql_database import SQLDatabase
from langchain.chat_models import AzureChatOpenAI
from langchain.agents.agent_toolkits import SQLDatabaseToolkit, create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain_community.tools.tavily_search import TavilySearchResults
import os 
import pandas as pd
import pyodbc 
from dotenv import load_dotenv

load_dotenv()


# Tavily Configuration
retriver = TavilySearchResults()

# Azure SQL Server Configuration
driver = "{ODBC Driver 18 for SQL Server}"
username = os.getenv('SQL_USERNAME')
server = f"tcp:{os.getenv('SQL_ENDPOINT')}"
password = os.getenv('SQL_PASSWORD')
database = os.getenv('SQL_DATABASE')

# file = pd.read_csv(r'C:\Users\v-abdullahma\Desktop\PythonTestFiles\LLMSQL\books\books.csv').fillna(value=0)

# print(file.head())

# #con = pyodbc.connect(r'Driver={ODBC Driver 18 for SQL Server};Server=tcp:ammysqldatabase.database.windows.net,1433;Database=LLMSQL;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
# con = pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}')  
# cursor = con.cursor()

# query_table = """
# CREATE TABLE Titanic (
#     PassengerId int PRIMARY KEY,
#     Survived bit NOT NULL,
#     Pclass int NOT NULL,
#     Name varchar(100) NOT NULL,
#     Sex varchar(10) NOT NULL,
#     Age float NULL,
#     SibSp int NOT NULL,
#     Parch int NOT NULL,
#     Ticket varchar(20) NOT NULL,
#     Fare float NOT NULL,
#     Cabin varchar(20) NULL,
#     Embarked char(1) NULL
# );
# """

# cursor.execute(query_table)

# for index, row in file.iterrows():
#      cursor.execute(
#     "INSERT INTO dbo.[Titanic] (PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked) values(?,?,?,?,?,?,?,?,?,?,?,?)",
#     row.PassengerId,
#     row.Survived,
#     row.Pclass,
#     row.Name,
#     row.Sex,
#     row.Age,
#     row.SibSp,
#     row.Parch,
#     row.Ticket,
#     row.Fare,
#     row.Cabin,
#     row.Embarked
# )

# con.commit()
# cursor.close()

# con = pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}')  
# cursor = con.cursor()
# print(cursor.execute("SELECT * FROM dbo.[Titanic]"))
# results = cursor.fetchall()

# for row in results:
#     print(row)

db_config = {
    'drivername': 'mssql+pyodbc', 
    'username': os.getenv('SQL_USERNAME') + '@' + os.getenv('SQL_ENDPOINT'), 
    'password': os.getenv('SQL_PASSWORD'), 
    'host': os.getenv('SQL_ENDPOINT'),
    'port': 1433, 
    'database': os.getenv('SQL_DATABASE'),
    'query': dict(driver='ODBC Driver 18 for SQL Server')
}

db_url = engine.URL.create(**db_config)
db = SQLDatabase.from_uri(db_url)

llm = AzureChatOpenAI(deployment_name="AMGPT4Turbo", temperature=0)
toolkit = SQLDatabaseToolkit(db=db, llm=llm) 

agent_executor = create_sql_agent(
    llm=llm, 
    toolkit=toolkit, 
    verbose=False, 
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
)


question = input("What is your query?\n")
while "exit" not in question:
    answer = agent_executor.invoke(question)['output']
    print(answer)
    question = input("Do you have other queries you would like answer for?\n")


# if "don't know." in answer:
#     response = retriver.invoke({"query":question, "search_depth":"advanced"})
#     url = response[0]['url']
#     print(url)
#     answer = response[0]['content']

# print(answer)
