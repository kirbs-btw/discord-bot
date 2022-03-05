import sqlite3
import datetime

def createSQL():
    # f = open("db.sql", "w+")
    conn = sqlite3.connect("db.sql")
    cur = conn.cursor()

    command = "CREATE TABLE daily(discord_id INT, daily_streak INT, last_daily DATE)"
    cur.execute(command)
    conn.commit()

def insertStuff():
    conn = sqlite3.connect("db.sql")
    cur = conn.cursor()

    command = "INSERT INTO daily VALUES(342766462819237866, 7, '2022-02-21')"
    cur.execute(command)
    conn.commit()

def delRow():
    conn = sqlite3.connect("db.sql")
    cur = conn.cursor()
    command = "DELETE FROM daily"
    cur.execute(command)
    conn.commit()
    print("done")

def printTable():
    conn = sqlite3.connect("db.sql")
    cur = conn.cursor()
    command = "SELECT * FROM daily"
    f = cur.execute(command).fetchall()
    for i in f:
        print(i)


def daily():
    conn = sqlite3.connect("wittu_bot_data.sql")
    cur = conn.cursor()
    command = "CREATE TABLE IF NOT EXISTS daily(discord_id INT, daily_streak INT, last_daily DATE)"
    cur.execute(command)
    conn.commit()

    discordId = 342766462819237866

    conn = sqlite3.connect("db.sql")
    cur = conn.cursor()

    today = datetime.date.today()
    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    # missing checks if existent
    userNotExist = False

    command = f"SELECT * FROM daily WHERE discord_id = '{discordId}'"
    userData = cur.execute(command).fetchall()
    if userData == []:
        userNotExist = True
    if userNotExist:
        command = f"INSERT INTO daily VALUES({discordId}, 1, '{today}')"
        cur.execute(command)
        conn.commit()
        printTable()
    else:
        userData = userData[0]
        streak = int(userData[1])
        lastDaily = userData[2]

        if str(lastDaily) == str(yesterday):
            streak += 1
        elif str(lastDaily) == str(today):
            pass
        elif str(lastDaily) != str(yesterday):
            streak = 1

        command = f"UPDATE daily SET daily_streak = '{streak}', last_daily = '{today}' WHERE discord_id = '{discordId}'"
        cur.execute(command)
        conn.commit()

if __name__ == '__main__':
    printTable()
    #delRow()
    #insertStuff()
    #printTable()
    #daily()
    #print("--")
    #printTable()