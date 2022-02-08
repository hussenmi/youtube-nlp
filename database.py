'''
Great medium article to set up PostgreSQL and pgAdmin (GUI for PostgreSQL)
https://towardsdatascience.com/a-practical-guide-to-getting-set-up-with-postgresql-a1bf37a0cfd7

Requirements:
- download postgreSQL and pgAdmin 4 https://www.postgresql.org/download/ 
- pip install SQLAlchemy
- pip install pandas

'''
from sqlalchemy import create_engine
import os

class DBconnector():

    def __init__(self, username="postgres", password="youtubenlp", host="localhost", port="5432") -> None:
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.con_url = "postgres://username:password@host:port/database"
        self.engine = create_engine(self.con_url)

    def execute_sql_query(self, sql) -> None:
        # input: SQL command as a string
        with self.engine.connect() as con:
            con.execute(sql)

    def execute_sql_from_file(self, sql_file) -> None:
        # read SQL script
        script_name = sql_file
        dirname = os.path.dirname(__file__)
        sql_file = os.path.join(dirname, script_name)

        sql = open(sql_file, 'r').read()

        try:
            # Executing SQL commands
            with self.engine.connect() as con:
                con.execute(sql)
            print(f'Successfully executed {script_name}')

        except Exception as err:
            print(f'Failed to execute {script_name}')
            print(f'Error:\n{err}')


# Load DataFrame into database: SQLAlchemy X Pandas
df.to_sql(
    name='table_name',
    con=engine,
    if_exists='append', # 'fail' raises exception if exists, 'replace' drops and recreates
    index=False)


from sqlalchemy import create_engine

# Connecting to Postgres
connection_uri = 'postgresql://postgres:test@localhost:5432/covid-19'
engine = create_engine(connection_uri)

with engine.connect() as con:
    result = con.execute(
                """
                SELECT
                    countries_and_territories,
                    SUM(cases) AS cases,
                    SUM(deaths) AS deaths
                FROM worldwide_cases
                GROUP BY countries_and_territories
                ORDER BY cases DESC
                """
                )

# returns a list of tuples 
for row in result.fetchall():
    print(row)


from sqlalchemy import create_engine
import pandas as pd
import os

# Connecting to Postgres
connection_uri = 'postgresql://postgres:test@localhost:5432/covid-19'
engine = create_engine(connection_uri)

# Reading our SQL script
script_name = 'query.sql'
dirname = os.path.dirname(__file__)
sql_file = os.path.join(dirname, script_name)
sql = open(sql_file, 'r').read()

# Reading query result into DataFrame
df = pd.read_sql(sql, engine)
print(df.head())