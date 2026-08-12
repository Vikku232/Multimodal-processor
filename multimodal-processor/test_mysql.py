import pymysql

try:
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="vikku@123",
        database="multimodal_processor"
    )

    print("MySQL connection successful!")

    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    print(cursor.fetchall())

    cursor.close()
    conn.close()

except Exception as e:
    print("MySQL connection failed:")
    print(type(e).__name__)
    print(e)