from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://shruti:shruti123@localhost:5432/aisqldb"

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:

    
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            department VARCHAR(100),
            salary INTEGER
        );
    """))

    
    connection.execute(text("""
        INSERT INTO employees (name, department, salary)
        VALUES
        ('Shruti', 'Data Science', 60000),
        ('Rahul', 'Backend', 75000),
        ('Ananya', 'AI Research', 90000);
    """))

    connection.commit()

print("Table created and sample data inserted successfully!")