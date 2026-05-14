from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://shruti:shruti123@localhost:5432/aisqldb"

engine = create_engine(DATABASE_URL)

try:
    connection = engine.connect()
    print("PostgreSQL connection successful!")
    connection.close()
except Exception as e:
    print("Connection failed:")
    print(e)