import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from psycopg2 import sql

try:
    connection = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
    db_exists = cursor.fetchone()

    if not db_exists:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
        connection.commit()
        print(f"Database '{DB_NAME}' created successfully.")
    else:
        print(f"Database '{DB_NAME}' already exists.")

    connection.close()
    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
    connection.commit()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id SERIAL PRIMARY KEY,
            post_id INTEGER NOT NULL,
            author VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE
        )
        """)
    connection.commit()

    print("Tables created successfully.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if connection:
        cursor.close()
        connection.close()
