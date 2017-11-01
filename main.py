# By: Shardul Shah and Ceegan Hale
# Go to end of code for things to add/questions

import sqlite3


def login(conn, user, passw):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agents WHERE aid=? and pwd=?", (user, passw))
    row = cursor.fetchone()
    conn.commit()

    if row is not None:
        return 1 # user is an agent

    cursor.execute("SELECT * FROM customers WHERE cid=? and pwd=?", (user, passw))
    row = cursor.fetchone()
    conn.commit()
    
    if row is not None:
        return 2 # user is a customer

    return 0 # user doesnt exist in DB
    
def cust_sign_up(conn, cid, name, address, pwd):
       # let c1 = cursor
       c1 = conn.cursor()
       # customer table only has primary key, so no need to PRAGMA foreign_keys = ON
       
       c1.execute("SELECT * FROM customers WHERE cid=:new_cid;", {"new_cid": cid})
       row = c1.fetchone() # c1.fetchone() returns none if there are no rows in the result table (that is, customer sign up cid is UNIQUE)
       
       if row is not None:
           return 0
    
       else:
           c1.execute("""INSERT INTO customers VALUES (?, ?, ?, ?);""", (cid, name, address, pwd))
           conn.commit()
           return 1
        
def add_tables(conn):
    c = conn.cursor()
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
      
      # the executescript along with mp1.db simply does the equivalent of this statement in the terminal: "sqlite3   a2.db   <a2-tables.sql"
      
    conn.commit() # save the tables in the DB ; actually commit the changes to the DB
      
    return
    
def test_data(conn):
     c = conn.cursor()
     
     c.executescript("""
       INSERT INTO agents VALUES
       ("a0", "Shardul Shah", "penguin");
       INSERT INTO customers VALUES
       ("c0", "Ceegan Hale", "50th Street NW", "bear");
       """) 
       # this executescript POPULATES data into our tables; the purpose is to add test data.
     conn.commit()
     
                     
def main():
    
    path = "./mp1.db" # establishes DB
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;') # turns on FKs for the DB for the rest of the connection
    conn.commit()
    username = ""
    password = ""
    
    # Following two lines creates and populates data into the database. Remove before submitting (I think. FIXME)
    add_tables(conn)
    test_data(conn)
    
    print("Welcome!")
    
    first_time_resp = input("Are you a first time user?(y/n)\n")
    
    while first_time_resp != 'y' and first_time_resp != 'n':
        print("\nPlease press y or n")
        first_time_resp = input("Are you a first time user?(y/n)\n")
        
    if first_time_resp == 'n':  # first_time_resp = 'n'
        resp = input("Would you like to login?(y/n)\n")
   
        while resp != 'y' and resp != 'n':
            print("\nPlease press y or n")
            resp = input("Would you like to login?(y/n)\n")
            # removes whitespace from input, may be unneeded since we are using the user to press either y or n:
            #for char in resp:
             #   if char != ' ' and char != '\n':
              #      resp = char
     
        if resp == 'y':
            username = input("Username: ")
            password = input("Password: ") 
            while login(conn, username, password) == 0:
                print("You entered your password or username incorrectly. Please try again.")
                username = input("Username: ")
                password = input("Password: ")
                # assuming first_time_user actually says yes to being first time.   
        else:
            print("Exit succesful")
            return
            
    else: # first_time_resp = 'y'
    
        new_acc_resp = input("Would you like to make a new account?(y/n)\n")
    
        while new_acc_resp != 'y' and new_acc_resp != 'n':
            print("\nPlease press y or n")
            new_acc_resp = input("Are you a first time user?(y/n)\n")
    
        if new_acc_resp == 'n':
            print("Exit succesful")
            return
        else:
            # note all agents are assumed to be registered, so there cannot be a new account being made for agents
            # making new account for customer:
            print("Please fill out the following required entries to sign up:\n")
            new_cid = input("Provide a customer ID:")    
            new_name = input("Enter your full name:")
            new_addr = input("Enter your address:")
            new_pwd = input("Enter a password for your account:")
            
            while cust_sign_up(conn, new_cid, new_name, new_addr, new_pwd) == 0:
                
                print("\nThe given ID is NOT unique.")
                new_cid = input("Please enter a unique customer ID\n")  
            
            print("Success! You have signed up.")
            
            # Is it ok if the user is automatically logged in after sign up?
            password = new_pwd
            username = new_cid            
    
    user_flag = login(conn, username, password)  
    # user_flag is the same as security level. That is:
    # if user_flag = 1, user is an agent
    # if user_flag = 2, user is a customer
    # if user_flag = 0, user is neither (should be impossible at this point according to our code)
         
    print("Security lvl: ", user_flag)
    
    if user_flag == 1:
        print("Welcome to the agent interface")
        # agent commands
    else:
        print("Welcome to the customer interface")

    
    conn.commit()    
    conn.close()

if __name__ == '__main__':
    main()
    
# Questions to ask prof:
    #   Is it ok if the user is automatically logged in after sign up?
    # What exactly is the prof looking for in the "exit the program" option?
    # Is the test gonna involve hard testing and trying to break EVERYTHING? Like, for example: first_time_user saying no, hes not one when in reality he is, which causes an infinite loop in the incorrect 'user/pass' section
    # Is the "y/n" way fine?
    # Do we remove our test data in the end before submitting? How will they add the data?

# Things to add: 
    # Bucket list
    # Agent commands
    # Customer commands
    # More Test data
    # Option to exit anytime
    