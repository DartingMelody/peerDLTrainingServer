import sqlite3
con = sqlite3.connect('metadata.db')
cur = con.cursor()
user_id = 1
rows = cur.execute("SELECT * FROM USERS")
for row in rows:
    print(row)
print("done")
jrows = cur.execute("SELECT * FROM JOBS")
for jrow in jrows:
    print(jrow)
#cur.execute("DELETE FROM USERS WHERE USER_ID = "+str(user_id))
con.commit()
con.close()
#cur.execute("UPDATE USERS SET MASTER_IP = (SELECT IP FROM USERS WHERE USER_ID ="+str(user_id)"+)" WHERE USER_ID ="+str(user_id))
