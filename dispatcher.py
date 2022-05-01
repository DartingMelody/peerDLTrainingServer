import sqlite3
import datetime
from math import trunc

con = sqlite3.connect('metadata.db',detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cur = con.cursor()
x = True
while(x):
    #x = False
    for row in cur.execute("SELECT * FROM JOBS WHERE STATUS IS 'READY' ORDER BY CREDITS DESC, JOB_DURATION ASC, NODES ASC, TIMESTAMP ASC LIMIT 5").fetchall():
        duration = row[2]
        job_id = row[0]
        nodes  = row[3]
        rows = cur.execute("SELECT USER_ID, IP FROM USERS WHERE STATUS = 'READY' AND MINUTES > "+str(duration) + " ORDER BY MINUTES ASC LIMIT "+str(nodes)).fetchall()
        if len(rows)<nodes:
            continue
        userids = ""
        for row in rows:
            userids = userids  + str(row[0])+","
        ranks = "(CASE "
        cnt = 0
        for row in rows:
            ranks = ranks + "WHEN USER_ID = "+str(row[0])+" THEN "+str(cnt)+" "
        ranks = ranks + "END )"
        master_ip = rows[0][1]
        cur.execute("UPDATE USERS SET JOB_ID = "+str(job_id) + ", RANK = "+ranks+", STATUS = 'RUNNING', MASTER_IP = '"+master_ip+"', WORLD_SIZE = "+str(nodes)+" WHERE USER_ID IN ("+userids[:-1]+")")
        cur.execute("UPDATE JOBS SET STATUS = 'RUNNING', START_TIMESTAMP = datetime('now','localtime') WHERE JOB_ID = "+str(job_id))
        print("running")
        con.commit()
    for row in cur.execute("SELECT USER_ID, JOB_ID, TIMESTAMP as '[timestamp]' FROM USERS WHERE STATUS = 'RUNNING' AND DATETIME(TIMESTAMP, '+2 minutes') < datetime('now','localtime')").fetchall():
        #print(row)
        job_row = cur.execute("SELECT START_TIMESTAMP as '[timestamp]', JOB_DURATION FROM JOBS WHERE JOB_ID = "+str(row[1])).fetchall()[0]
        #mints = job_row[1] - job_row[2] #(ROUND((JULIANDAY(row[2]) - JULIANDAY(job_row[0])) * 14400))
        mints = job_row[1] - trunc((row[2]-job_row[0]).total_seconds() / 60)
        print(mints)
        if mints > 0:
            cur.execute("UPDATE JOBS SET STATUS = 'READY', JOB_DURATION = "+str(mints)+" WHERE STATUS = 'RUNNING' AND JOB_ID="+str(row[1]))
            #cur.execute("UPDATE USERS SET STATUS = 'INACTIVE' WHERE USER_ID = "+row[0])
        else:
            cur.execute("UPDATE JOBS SET STATUS = 'DONE' WHERE STATUS = 'RUNNING' AND JOB_ID="+str(row[1]))
        cur.execute("UPDATE USERS SET STATUS = 'INACTIVE' WHERE USER_ID = "+str(row[0]))
        con.commit()
