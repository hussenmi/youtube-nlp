'''
Great medium article to set up PostgreSQL and pgAdmin (GUI for PostgreSQL)
https://towardsdatascience.com/a-practical-guide-to-getting-set-up-with-postgresql-a1bf37a0cfd7

Requirements:
- download postgreSQL and pgAdmin 4 https://www.postgresql.org/download/ 
- pip install SQLAlchemy
- pip install pandas

'''
from sqlalchemy import create_engine
import pandas as pd
import os

class DBconnector():

    def __init__(self, username="postgres", password="youtubenlp", host="localhost", port="5432") -> None:
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.con_url = f"postgres://{username}:{password}@{host}:{port}/database"
        self.engine = create_engine(self.con_url)

    def execute_sql_query(self, sql_query) -> None:
        """ Executes a sql query"""
        with self.engine.connect() as con:
            con.execute(sql_query)

    def execute_sql_from_file(self, sql_file) -> None:
        """ Executes a sql query from a sql script/file """
        script_name = sql_file
        dirname = os.path.dirname(__file__)
        sql_file = os.path.join(dirname, script_name)

        sql = open(sql_file, 'r').read()

        try:
            # execute SQL commands
            with self.engine.connect() as con:
                con.execute(sql)
            print(f'Successfully executed {script_name}')

        except Exception as err:
            print(f'Failed to execute {script_name}')
            print(f'Error:\n{err}')

    def insert_dataframe(self, dataframe, table_name) -> None:
        """ Inserts pandas dataframe into a postgreSQL database table"""
        dataframe.to_sql(
            name = table_name, 
            con = self.engine, 
            if_exists = 'append', # 'fail' raises exception, 'replace' drops and recreates
            index = True) # dataframe index as column

    def fetch_dataframe_from_query(self, dataframe, sql_query) -> pd.DataFrame:
        """ Reads a select SQL query into a pandas dataframe"""
        dataframe = pd.read_sql(sql_query, self.engine)
        return dataframe

    def fetch_rows_from_query(self, sql_query) -> list:
        """ Reads a select SQL query and returns a list of tuples """
        with self.engine.connect() as con:
            result = con.execute(sql_query)
        return result.fetchall()