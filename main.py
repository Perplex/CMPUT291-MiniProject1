import sqlite3


def login(conn, user, passw):
    cursor = conn.execute("SELECT aid, pwd from agents WHERE aid=? and pwd=?", (user, passw))

    if cursor.rowcount != -1:
        return 1

    cursor = conn.execute("SELECT aid, pwd from agents WHERE aid=? and pwd=?", (user, passw))
    if cursor.rowcount != -1:
        return 2

    return 0


def main():

    conn = sqlite3.connect("mp1.db")

    resp = input("Would you like to login?(y/n)")

    if resp == 'y':
        username = input("Username: ")
        password = input("Password: ")

        print("Security lvl: ", login(conn, username, password))

    conn.close()

if __name__ == '__main__':
    main()
