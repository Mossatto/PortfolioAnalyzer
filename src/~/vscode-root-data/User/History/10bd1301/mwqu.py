import psycopg2
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

try:
    # Conexão com o PostgreSQL
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    print("✅ PostgreSQL connection established successfully.")

    cur = conn.cursor()


    conn.commit()
    print("✅ Tables checked/created successfully.")

    # Inserção de dados de teste
    try:
        cur.execute('INSERT INTO "user" (user_name) VALUES (%s) RETURNING id;', ("Matheus",))
        user_id = cur.fetchone()[0]

        cur.execute(
            'INSERT INTO "project" (user_id, project_name) VALUES (%s, %s);',
            (user_id, "Projeto de Teste")
        )

        conn.commit()
        print("✅ Data inserted successfully.")

    except Exception as e:
        conn.rollback()
        print("❌ Error during data insertion. Operation ROLLED BACK:", e)

    cur.close()
    conn.close()

except Exception as e:
    print("❌ Error connecting to PostgreSQL. Check your .env credentials and DB status. Details:", e)
