# AOAI-Langchain-SQL
In this repo, I am using GPT-4 turbo from Azure OpenAI, Azure SQL database and langchain to answer user's questions based on the information available on the SQL database. 

You can use the following links to create the requried resources: 
1) [Create Azure OpenAI Resource](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal)
2) [Create Azure SQL Database](https://learn.microsoft.com/en-us/azure/azure-sql/database/single-database-create-quickstart?view=azuresql&tabs=azure-portal) 

# Table of contents:
- [Step 1 - Installing the Requirements and Gettings Things Ready]
- [Step 2 - Loading the csv file data to Azure SQL database]
- [Step 3 - Configuring Chatbot]
- [Step 4 - Running the code] 


## Step 1 - Installing the Requirements and Gettings Things Ready

1. Initally, we would need to install the necessary python libraries for Azure OpenAI, dotenv, langchain, panadas, and sqlalchemy. 
Run the following command to install all required libraries: 
```
pip install -r requirements.text
```
2. You need to create .env file that will contain all the information related to your Azure OpenAI models.  
You can get the information related to the SQL database from the connection string tab for the SQL database on Azure portal as shown below:
![Sql_information](Images/SQL_Info.png).
From the above image you can find a link to download the necceary driver for the ODBC servce. This driver will allow you to connect to the Azure SQL database. 
Be sure to download the **ODBC Driver 18** 

4. Fill out your .env details as shown below:  
![Environment Variables](Images/EnvVariables.png)

## Step 2 - Loading the csv file data to Azure SQL database:
This class will be used to create table, insert data, and load data from the SQL database. 
1. The create_engine() is the first function in the class that is used to create the connection to the Azure SQL database as shown belwo: 
``` python
def create_engine(self):  
        username = os.getenv('SQL_USERNAME')  
        password = os.getenv('SQL_PASSWORD')  
        server = f"tcp:{os.getenv('SQL_ENDPOINT')}"
        database = os.getenv('SQL_DATABASE')  
        driver = "ODBC Driver 18 for SQL Server"  
        connection_string = f"mssql+pyodbc:///?odbc_connect=DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"  
        engine = create_engine(connection_string)  
        return engine
```

2. The create_table(), insert data() functions will be used to get the data from the loaded csv file and inserting the csv file contents in the database. User can define the name of the created table.
``` python
    def create_table(self, table_name):  
        # Use SQLAlchemy to generate the table schema from the dataframe  
        self.df.to_sql(table_name, self.engine, if_exists='replace', index=False)  
        print(f"Table {table_name} has been created in the database.")
      
    def insert_data(self, table_name):  
        # Use pandas to_sql method for inserting the data  
        self.df.to_sql(table_name, self.engine, if_exists='append', index=False)  
        print(f"Data has been inserted into {table_name} table.")
```
3. The read_db() function will be used to return an SQLDatabase from the engine connection so that it can be used as an sql database in the sql_agent:
``` python
def read_db(self):
        return SQLDatabase(self.engine)
```

## Step 3 Configuring Chatbot: 


## Step 4 - Running the code: 



