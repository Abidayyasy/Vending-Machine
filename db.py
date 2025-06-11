import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=" 34.126.94.46",
        user="admin_fm",
        password="1234567890",  # ganti kalau pakai password
        database="fending_machine"
    )
