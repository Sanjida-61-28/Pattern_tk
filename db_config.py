import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # default in XAMPP
        database="remote_tracker"
    )
