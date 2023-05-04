import os
import sys
import log
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name  # connects to existing db, create first in IDE or separate script
        )
        print("Connection to MySQL DB successful")
        # print(connection)
    except Error as e:
        print(log.warning(f"The error '{e}' occurred"))

    return connection


def create_db(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database successfully created")
    except Error as e:
        print(log.warning(f"The error '{e}' occurred"))


if __name__ == "__main__":
    load_dotenv()

    user_pass = os.environ.get("my_sql_pass")
    log = log.logger
    connection = create_connection(
        'localhost', 'root', user_pass, 'automated_db1')
    create_db_query = "CREATE DATABASE automated_db1"
    create_db(connection, create_db_query)

    # print(connection.cursor())
