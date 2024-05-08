"""import psycopg2 to connect to PostreSQL database"""
import os #módulo os para interactuar con las variables de entorno
import psycopg2 #PostgreSQL database adapter for Python
from dotenv import load_dotenv
load_dotenv()

try:
    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname = os.getenv("POSTGRES_DATABASE"),
        port="5432", #el puerto por defecto de PostgreSQL es 5432
    )
    print("Conexión exitosa a la base de datos.")
except psycopg2.Error as e:
    print("Error al conectarse a la base de datos:", e)
    