import sqlite3

def main():
    conn = sqlite3.connect("db.sql")
    cur = conn.cursor()

    command = "CREATE TABLE IF NOT EXISTS userData(id INT, money INT)"
    cur.execute(command)
    conn.commit()

    print("DONE")

if __name__ == '__main__':
    main()

