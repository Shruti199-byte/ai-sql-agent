from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://shruti:shruti123@localhost:5432/aisqldb"

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    connection.execute(text("""
                         
        DROP TABLE IF EXISTS marks;
        DROP TABLE IF EXISTS students;
        DROP TABLE IF EXISTS sections;
        DROP TABLE IF EXISTS batches;
    """))

    connection.execute(text("""
        CREATE TABLE batches (
            id SERIAL PRIMARY KEY,
            batch_name VARCHAR(100) NOT NULL
        );
    """))

    connection.execute(text("""
        CREATE TABLE sections (
            id SERIAL PRIMARY KEY,
            section_name VARCHAR(50) NOT NULL,
            batch_id INTEGER REFERENCES batches(id)
        );
    """))

    connection.execute(text("""
        CREATE TABLE students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            section_id INTEGER REFERENCES sections(id)
        );
    """))

    connection.execute(text("""
        CREATE TABLE marks (
            id SERIAL PRIMARY KEY,
            student_id INTEGER REFERENCES students(id),
            subject VARCHAR(100),
            marks INTEGER
        );
    """))

    connection.execute(text("""
        INSERT INTO batches (batch_name)
        VALUES ('BTech CSE 2026');
    """))

    connection.execute(text("""
        INSERT INTO sections (section_name, batch_id)
        VALUES
        ('A', 1),
        ('B', 1);
    """))

    connection.execute(text("""
        INSERT INTO students (name, section_id)
        VALUES
        ('Shruti', 1),
        ('Rahul', 1),
        ('Ananya', 1),
        ('Karan', 1),
        ('Meera', 1),
        ('Riya', 2),
        ('Aman', 2),
        ('Neha', 2),
        ('Kabir', 2),
        ('Tanya', 2);
    """))

    connection.execute(text("""
        INSERT INTO marks (student_id, subject, marks)
        VALUES
        (1, 'DBMS', 88), (1, 'Python', 92),
        (2, 'DBMS', 75), (2, 'Python', 80),
        (3, 'DBMS', 95), (3, 'Python', 97),
        (4, 'DBMS', 60), (4, 'Python', 65),
        (5, 'DBMS', 84), (5, 'Python', 86),
        (6, 'DBMS', 90), (6, 'Python', 91),
        (7, 'DBMS', 70), (7, 'Python', 73),
        (8, 'DBMS', 78), (8, 'Python', 82),
        (9, 'DBMS', 55), (9, 'Python', 60),
        (10, 'DBMS', 89), (10, 'Python', 87);
    """))

    connection.commit()

print("University database created successfully!")