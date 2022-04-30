import sqlite3
con = sqlite3.connect('metadata.db')
cur = con.cursor()
cur.execute('''CREATE TABLE USERS
                       ( USER_ID INTEGER primary key autoincrement, SPEC text, MINUTES real, TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP, STATUS text, IP text, MASTER_IP text, WORLD_SIZE text, RANK text, JOB_ID real)''')
cur.execute('''CREATE TABLE JOBS
                               ( JOB_ID INTEGER primary key autoincrement, CREDITS real, JOB_DURATION real, NODES real, TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP, START_TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP, STATUS text)''')
con.commit()
con.close()
