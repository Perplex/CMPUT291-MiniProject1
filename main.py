import sqlite3


def login(cursor, conn, user, passw):
    cursor.execute("SELECT * from agents WHERE aid=? and pwd=?", (user, passw))
    row = cursor.fetchone()
    conn.commit()

    if row is not None:
        return 1

    cursor.execute("SELECT * from customers WHERE cid=? and pwd=?", (user, passw))
    row = cursor.fetchone()
    conn.commit()
    
    if row is not None:
        return 2

    return 0


def main():
    
    path = "./mp1.db"
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')
    conn.commit()
    
    # note in the below statement, need """ to allow for multiple line script in python"""
    c.executescript("""drop table if exists deliveries;
    drop table if exists olines;
    drop table if exists orders;
    drop table if exists customers;
    drop table if exists carries;
    drop table if exists products;
    drop table if exists categories;
    drop table if exists stores;
    drop table if exists agents;

    create table agents (
      aid           text,
      name          text,
      pwd       	text,
      primary key (aid));
    create table stores (
      sid		int,
      name		text,
      phone		text,
      address	text,
      primary key (sid));
    create table categories (
      cat           char(3),
      name          text,
      primary key (cat));
    create table products (
      pid		char(6),
      name		text,
      unit		text,
      cat		char(3),
      primary key (pid),
      foreign key (cat) references categories);
    create table carries (
      sid		int,
      pid		char(6),
      qty		int,
      uprice	real,
      primary key (sid,pid),	
      foreign key (sid) references stores,
      foreign key (pid) references products);
    create table customers (
      cid		text,
      name		text,
      address	text,
      pwd		text,
      primary key (cid));
    create table orders (
      oid		int,
      cid		text,
      odate		date,
      address	text,
      primary key (oid),
      foreign key (cid) references customers);
    create table olines (
      oid		int,
      sid		int,
      pid		char(6),
      qty		int,
      uprice	real,
      primary key (oid,sid,pid),
      foreign key (oid) references orders,
      foreign key (sid) references stores,
      foreign key (pid) references products);
    create table deliveries (
      trackingNo	int,
      oid		int,
      pickUpTime	date,
      dropOffTime	date,
      primary key (trackingNo,oid),
      foreign key (oid) references orders);""")
      
    c.executescript("""
      INSERT INTO agents VALUES
      ("a0", "Shardul Shah", "penguin");
      INSERT INTO customers VALUES
      ("c0", "Ceegan Hale", "50th Street NW", "bear");
      
      """)
  
    conn.commit()
    # the executescript along with mp1.db simply does the equivalent of this statement in the terminal: "sqlite3   a2.db   <a2-tables.sql"

    resp = input("Would you like to login?(y/n)")
    
    # removes whitespace from input : 
    for char in resp:
        if char != ' ' and char != '\n':
            resp = char
    
    while resp != 'y' and resp != 'n':
        print("Please press y or n")
        resp = input("Would you like to login?(y/n)")
        # removes whitespace from input, may be unneeded since we are using the user to press either y or n:
        #for char in resp:
         #   if char != ' ' and char != '\n':
          #      resp = char
                 
    if resp == 'y':
        username = input("Username: ")
        password = input("Password: ")    
    else:
        print("Exit succesful")
        return

    print("Security lvl: ", login(c, conn, username, password))

    conn.commit()    
    conn.close()

if __name__ == '__main__':
    main()