import sqlite3
import datetime
from math import trunc
import math
import datetime

con = sqlite3.connect('metadata.db',detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cur = con.cursor()
x = True
while(x):
    rows1 = cur.execute("SELECT USER_ID, START_TIMESTAMP, DURATION, SPEC, CREDIT FROM CREDITS ORDER BY CREDIT DESC, DURATION ASC, SPEC DESC, START_TIMESTAMP ASC").fetchall()
    for row in row1:
        user_id = row[0]
        u_row = cur.execute("SELECT MINUTES, TIMESTAMP FROM USERS WHERE USER_ID = "+str(user_id)).fetchall()[0]
        mints = trunc((u_row[1]-row[1]).total_seconds())/60 - u_row[0]
        mints_done = row[2]-u_row[0]
        jrows = cur.execute("SELECT JOB_DURATION, JOB_ID FROM JOBS WHERE USER_ID = "+str(user_id))+" WHERE STATUS = 'RUNNING'").fetchall()
        credit_cons = 0
        for jrow in jrows:
            urow = cur.execute("SELECT MINUTES FROM USERS WHERE JOB_ID = "+str(job_id)).fetchall()
            for ur in urow:
                credit_cons = credit_cons + (jrow[0]-urow[0])*spec
        cur.execute("UPDATE CREDITS SET CREDIT = "+str(row[4]+(mints_done - 0.2*mints)*spec - credit_cons)+ ", DURATION = "+str(mints)+", START_TIMESTAMP = CURRENT_TIMESTAMP")
        con.commit()
    time.sleep(5*60)
