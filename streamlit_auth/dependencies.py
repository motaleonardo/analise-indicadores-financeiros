import psycopg2
from dotenv import load_dotenv, find_dotenv
import os
from contextlib import contextmanager

load_dotenv(find_dotenv())

database = os.getenv('DATABASE')
host = os.getenv('HOST')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
port = os.getenv('PORT')

@contextmanager
def instance_cursor():
    connection = psycopg2.connect(database=database, host=host, user=username, password=password, port=port)
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print('Conexão com o Banco de Dados fechada')