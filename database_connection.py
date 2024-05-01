import mysql.connector

def db_connect():
    try:
        # Connect to MySQL database
        db = mysql.connector.connect(
            host="soccer12.c1ek82uiqfgh.ap-south-1.rds.amazonaws.com",
            user="admin",
            passwd="soccerplayer",
            database="soccer"
        )
        
        if db.is_connected():
            print("Connected to MySQL database")
        
        return db
    except mysql.connector.Error as e:
        print("Error connecting to MySQL database:", e)
        return None
