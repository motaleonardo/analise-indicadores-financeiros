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

def consulta_geral():
    with instance_cursor() as cursor:
        query = '''
            SELECT *
            FROM USUARIOS
        '''
        cursor.execute(query)
        request = cursor.fetchall()
        return request
    
def consulta_nome(user):
    with instance_cursor() as cursor:
        query = '''
            SELECT name, username, password
            FROM USUARIOS
            WHERE username = %s
        '''
        cursor.execute(query, (user,))
        request = cursor.fetchall()
        return request
    
def create_table():
    connection = psycopg2.connect(database=database, host=host, user=username, password=password, port=port)
    cursor = connection.cursor()

    query = '''
        CREATE TABLE IF NOT EXISTS USUARIOS (
            id serial PRIMARY KEY,
            name varchar(255),
            username varchar(255),
            password varchar(255),
            email varchar(255),
            created_at timestamp,
            admin boolean DEFAULT FALSE,
            UNIQUE (username)
        )
    '''
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    print('Tabela USUARIOS criada com sucesso')


def add_registro(name, user, passw, email, created_at):
    connection = psycopg2.connect(database=database, host=host, user=username, password=password, port=port)
    cursor = connection.cursor()

    query = '''
        INSERT INTO USUARIOS (name, username, password, email, created_at)
        VALUES (%s, %s, %s, %s, %s)
    '''

    cursor.execute(query, (name, user, passw, email, created_at))
    connection.commit()
    if connection:
        cursor.close()
        connection.close()
        print('Conexão com o Banco de Dados fechada')
