# AOAI-Langchain-SQL

# Table of contents:
- [Step 1 - Installing the Requirements and Gettings Things Ready]


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



