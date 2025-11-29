import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# ============================================
#  Cargar variables de entorno
# ============================================
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

SCHEMA_PATH = "/database/schema.sql"


def run_schema():
    print("📦 Cargando archivo schema.sql ...")

    if not os.path.exists(SCHEMA_PATH):
        raise FileNotFoundError(f"No se encontró schema.sql en {SCHEMA_PATH}")

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    print("🔗 Conectando a PostgreSQL...")

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    conn.autocommit = True
    cur = conn.cursor()

    print("🚀 Ejecutando script SQL...")
    cur.execute(schema_sql)

    cur.close()
    conn.close()

    print("✅ Base de datos inicializada correctamente.")


if __name__ == "__main__":
    try:
        run_schema()
    except Exception as e:
        print("❌ Error inicializando la base de datos:")
        print(e)
