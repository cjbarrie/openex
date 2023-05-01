import pandas as pd
import sqlite3
conn = sqlite3.connect('instance/responses.db', isolation_level=None)
conn.execute("PRAGMA foreign_keys = ON;")
df = pd.read_sql_query('SELECT * FROM survey_response', conn)
conn.close()
print(df)
