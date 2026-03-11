import pymysql
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


connection = pymysql.connect(
    host= DB_HOST,
    user= DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

print("Database connection successful!")
connection.close()