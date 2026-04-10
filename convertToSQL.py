import pandas as pd
from sqlalchemy import create_engine

# Define your database connection details
db_user = 'username'
db_password = 'password'
db_host = '127.0.0.1'  # or 'localhost'
db_port = '3306'  # default MySQL port
db_name = 'CBFP'

# Create a connection string
connection_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# Create an SQLAlchemy engine
engine = create_engine(connection_string)

# Read the CSV file into a pandas DataFrame
csv_file_path = 'Cleaned_Dataset/Barrie_population_demographics_aged_above_65.csv'
df = pd.read_csv(csv_file_path)

# Write the DataFrame to a SQL table
table_name = 'Population'
df.to_sql(table_name, con=engine, if_exists='replace', index=False)

print(f"Data from {csv_file_path} has been successfully written to the table {table_name} in the database {db_name}.")
