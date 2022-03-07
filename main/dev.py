import sqlite3

def main():
    conn = sqlite3.connect("db.sql")
    cur = conn.cursor()
    command = "UPDATE userData SET money = '1070997' WHERE id = '427902023321518080'"
    cur.execute(command)
    conn.commit()
    conn.close()


def resetUsers():
    conn = sqlite3.connect("db.sql")
    cur = conn.cursor()
    command = "UPDATE userData SET money = '1000'"
    cur.execute(command)
    conn.commit()
    conn.close()


def readDB():
    conn = sqlite3.connect("db.sql")
    cur = conn.cursor()
    command = "SELECT * FROM userData"
    data = cur.execute(command).fetchall()
    for i in data:
        print(i)


if __name__ == '__main__':
    resetUsers()
    #readDB()