# medium https://towardsdatascience.com/a-practical-guide-to-getting-set-up-with-postgresql-a1bf37a0cfd7

# download postgresql and pgAdmin 4

# pip install SQLAlchemy

# Connecting to Postgres default username: postgres; localhost:5432
from sqlalchemy import create_engine
connection_uri = 'postgres://username:password@host:port/database'
engine = create_engine(connection_uri)

# Executing SQL command
with engine.connect() as con:
    con.execute(sql)

from sqlalchemy import create_engine
import os

# Connecting to Postgres
connection_uri = 'postgresql://postgres:test@localhost:5432/covid-19'
engine = create_engine(connection_uri)

# Reading our SQL script
script_name = 'create_table.sql'
dirname = os.path.dirname(__file__)
sql_file = os.path.join(dirname, script_name)

sql = open(sql_file, 'r').read()

try:
    # Executing SQL commands
    with engine.connect() as con:
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