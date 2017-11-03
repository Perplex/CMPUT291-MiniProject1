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
     
    c.executescript(
    """
        INSERT INTO stores VALUES
            (0, "Sobeys Namao", '(780) 473-3442', "9611 167 Ave NW"),
            (1, "M&M Food Market", "(780) 475-5452", "16528 95 St"),
            (2, "Elsafadi Supermarket", "(780) 406-3617", "10807 Castle Downs Rd NW"),
            (3, "Walmart", "(780) 457-4366", "16940 127 St NW"),
            (4, "Save-On-Foods", "(780) 472-7400", "9510 160 Ave NW"),
            (5, "T&T Supermarket", "(780) 409-8686", "9450 137 Ave NW"),
            (6, "Walmart", "(780) 406-8807", "9402 135 Ave"),
            (7, "Superstore", "(780) 406-3768", "12350 137 Ave NW");

        -- Schema: cat* (char3), name (text)
        INSERT INTO categories VALUES
            ('bak', 'dakery'),
            ('pro', 'produce'),
            ('del', 'deli'),
            ('mea', 'meat'),
            ('she', 'shelf'),
            ('fro', 'frozen'),
            ('dai', 'dairy'),
            ('oth', 'other');

        -- Schema: pid* (char6), name (text), unit (text), cat (char3)
        INSERT INTO products VALUES 
            ("bak0", "Bread, White, Sliced", "ea", "bak"),
            ("bak1", "Bagel, Everything, 6-pack", "ea", "bak"),
            ("bak2", "Pitas, Whole Wheat, 8-pack", "ea", "bak"),
            ("pro0", "Garlic, 3-pack", "ea", "pro"),
            ("pro1", "Cucumber, English", "ea", "pro"),
            ("pro2", "Tomato, Vine-Ripened", "kg", "pro"),
            ("pro9", "Baby Bok Choy", "kg", "pro"),
            ("del0", "Prosciutto, Sliced", "kg", "del"),
            ("del1", "Gouda, Mild", "ea", "del"),
            ("del2", "Guanciale", "kg", "del"),
            ("del9", "Jarlsberg", "kg", "del"),
            ("mea0", "Chicken Breasts", "kg", "mea"),
            ("mea1", "Chicken Thighs", "kg", "mea"),
            ("mea2", "Applewood Bacon", "ea", "mea"),
            ("mea9", "Pork Belly", "ea", "mea"),
            ("she0", "Spaghetti, Whole Wheat", "ea", "she"),
            ("she1", "Mayonnaise, Half-Fat, Jar", "ea", "she"),
            ("she2", "Coke Zero, Bottled, 6-pack", "ea", "she"),
        --     ("fro0", "Pizza, Margherita", "ea", "fro"),
        --     ("fro1", "Prime Burgers, 8-pack", "ea", "fro"),
        --     ("fro2", "Ice Cream, Mint Chocolate Chip", "ea", "fro"),
            ("dai0", "Milk, Whole, Jug", "ea", "dai"),
            ("dai1", "Greek Yogurt, 5%, Tub", "ea", "dai"),
            ("dai2", "Sour Cream, 2%, Tub", "ea", "dai"),
            ("oth0", "Socks, Ankle, 6-pack", "ea", "oth"),
            ("oth1", "Gift Card, $20", "ea", "oth"),
            ("oth2", "Headphones", "ea", "oth"),
            ("oth9", "PlayStation 4", "ea", "oth");

        -- Schema: sid* (int), pid* (char6), qty (int), uprice (real)
        INSERT INTO carries VALUES
            /* Unique Stock Cases: T&T has two unique items */
            (3, "oth9", 5, 399.99),
            (7, "del9", 10, 8.99),
            (5, "mea9", 15, 3.99),
            (5, "pro9", 20, 1.99),

            (0, "bak0", 10, 3.29),
            (0, "bak1", 25, 4.99),
            (0, "bak2", 33, 5.99),
            (0, "del0", 50, 3.99),    
            (0, "mea1", 47, 12.99),
            (0, "mea2", 43, 6.99),
            (0, "dai0", 80, 5.29),
            (0, "dai1", 5, 5.89),
            (0, "dai2", 50, 3.99),
            (0, "oth0", 10, 6.99),
    
            (1, "bak0", 20, 3.99),
            (1, "bak1", 5, 5.99),
            (1, "bak2", 23, 5.99),
            (1, "mea1", 500, 11.23),
            (1, "mea2", 38, 7.27),
            (1, "dai1", 17, 5.99),

            (2, "del0", 5, 4.22),
            (2, "dai1", 12, 6.23),
            (2, "dai2", 33, 3.69),
            (2, "mea1", 56, 13.00),
    
            (3, "mea1", 99, 12.99),
            (3, "oth0", 12, 7.99),

            (4, "mea1", 17, 12.99),

            (6, "dai1", 99, 5.99),
            (6, "mea1", 200, 12.99),
    
            (7, "dai0", 23, 5.19),
            (7, "mea1", 20, 12.99),
            (7, "oth0", 200, 7.99);

        -- Schema: cid* (text), name (text), address (text)
        INSERT INTO customers VALUES
            ("c0", "David Chang", "His House, Probably", "pw0"),
            ("c1", "Anthony Bourdain", "Not Edmonton", "pw1"),
            ("c2", "Wolfgang Puck", "Chez Puck", "pw2"),
            ("c3", "Emeril Lagasse", "Everywhere", "pw3"),
            ("c4", "Rich Moonen", "Middle of the Ocean", "pw4"),
            ("c5", "Chris Cosentino", "On a Farm", "pw5"),
            ("c6", "J. Kenji Lopez-Alt", "In a Lab, Maybe", "pw6"),
            ("c7", "John Besh", "Swamp", "pw7"),
            ("c8", "Guy Fieri", "Nobody Cares", "pw8"),
            ("c9", "John Doe", "Nowhere", "pw9"),
            ("c10", "Sash Same", "50th Street NW", "pw10");

        -- Schema: oid* (int), cid (text), odate (date), address (text)
        INSERT INTO orders VALUES
            (1000, "c0", DATETIME("now", "-8 days"), "His House, Probably"),
            (1001, "c0", DATETIME("now", "-6 days"), "His House, Probably"),
            (1010, "c1", DATETIME("now", "-5 days"), "Not Edmonton"),
            (1011, "c1", DATETIME("now", "-2 days"), "Not Edmonton"),
            (1020, "c2", DATETIME("now", "-6 days"), "Chez Puck"),
            (1021, "c2", DATETIME("now", "-1 days"), "Chez Puck"),
            (1030, "c3", DATETIME("now", "-3 days"), "Everywhere"),
            (1031, "c3", DATETIME("now", "-2 days"), "Everywhere"),
            (1040, "c4", DATETIME("now", "-13 days"), "Middle of the Ocean"),
            (1041, "c4", DATETIME("now", "-5 days"), "Middle of the Ocean"),
            (1050, "c5", DATETIME("now", "-7 days"), "On a Farm"),
            (1051, "c5", DATETIME("now", "-1 days"), "On a Farm"),
            (1060, "c6", DATETIME("now", "-20 days"), "In a Lab, Maybe"),
            (1061, "c6", DATETIME("now", "-10 days"), "In a Lab, Maybe"),
            (1070, "c7", DATETIME("now", "-5 hours"), "Swamp"),
            (1071, "c7", DATETIME("now", "-2 hours"), "Swamp"),
            (1080, "c8", DATETIME("now", "-5 days"), "Nobody Cares"),
            (1081, "c8", DATETIME("now", "-4 days"), "Nobody Cares"),
            (1090, "c9", DATETIME("now"), "Nowhere"),
            (1091, "c9", DATETIME("now", "-1 hour"), "Nowhere"),
            (1092, "c9", DATETIME("now", "-2 days"), "Nowhere");
    

        -- Schema: oid* (int), sid* (int), pid* (char6), qty (int), uprice (real)
        INSERT INTO olines VALUES

            /* 1000: Same dairy, different stores */
            (1000, 0, "dai1", 1, 5.89),
            (1000, 2, "dai1", 1, 6.23),
            (1000, 4, "mea1", 2, 12.99),
            (1000, 7, "oth0", 1, 7.99),
            (1001, 0, "mea1", 1, 12.99),
            (1001, 7, "del9", 1, 7.99),
    
            /* 1010, 1011: All orders with one store, not Walmart*/
            (1010, 7, "mea1", 1, 12.99),
            (1010, 7, "oth0", 1, 7.99),
            (1010, 7, "del9", 1, 7.99),
            (1011, 7, "mea1", 1, 12.99),
            (1011, 7, "del9", 1, 7.99),

            /* 1020, 1021: Different dairy, different stores, different orders */    
            (1020, 6, "dai1", 2, 5.99),
            (1020, 7, "oth0", 1, 7.99),
            (1020, 7, "del9", 1, 7.99),
            (1021, 0, "dai2", 5, 3.99),
    
            /* 1030: All orders with one store, all one Walmart */
            (1030, 3, "mea1", 2, 12.99),
            (1030, 3, "oth0", 1, 7.99),
            (1030, 3, "del9", 1, 7.99),
            (1031, 3, "mea1", 1, 12.99),
    
            /* 1041: Different dairy, same store */
            (1040, 1, "mea1", 5, 11.23),
            (1040, 7, "oth0", 1, 7.99),
            (1041, 0, "dai0", 2, 5.29),
            (1041, 0, "dai1", 3, 5.89),
            (1041, 2, "mea1", 4, 13.00),
            (1041, 7, "del9", 1, 7.99),
    
            /* 1051, 1051: All orders with Walmart, two different locations */
            (1050, 3, "mea1", 1, 12.99),
            (1050, 6, "del2", 1, 7.99),
            (1050, 3, "oth0", 1, 7.99),
            (1051, 6, "mea1", 1, 12.99),
            (1051, 3, "del2", 1, 7.99),
    
            /* 1060: Different dairy, different stores */
            (1060, 0, "dai2", 2, 3.99),
            (1060, 7, "oth0", 1, 7.99),
            (1060, 7, "dai0", 1, 5.19),
            (1061, 0, "mea1", 1, 12.99),
    
            /* 1070: All orders with one store, not Walmart */
            (1070, 0, "mea1", 1, 11.23),
            (1070, 0, "oth0", 1, 6.99),
            (1071, 0, "mea1", 1, 11.23),
        --     (1072, 0, "del0", 2, 3.99),
        --     (1073, 0, "mea2", 5, 6.99),
    
            /* 1080: Every dairy, multiple stores */
            (1080, 0, "dai0", 1, 5.50),
            (1080, 1, "dai1", 1, 5.99),
            (1080, 2, "dai2", 1, 3.69),
            (1080, 0, "dai1", 2, 5.89),
            (1080, 0, "mea1", 1, 12.99),
            (1080, 7, "oth0", 1, 7.99),
            (1081, 0, "mea1", 1, 12.99),
            (1081, 7, "del9", 1, 7.99),
    
            /* All orders not with Walmart but not one store */
            (1090, 0, "mea1", 1, 1.99),
            (1090, 7, "oth0", 1, 1.99),
            (1091, 0, "mea1", 1, 1.99),
            (1092, 0, "mea1", 1, 1.99),
            (1092, 0, "del9", 1, 1.99);
    
        -- trackingNo* (int), oid* (int), pickUpTime (date), dropOffTime (date)
        INSERT INTO deliveries VALUES
            /* JOHN DOE tests: 190 fits, 191 and 192 don't */
            (190, 1090, DATETIME("now"), NULL),
            (191, 1091, DATETIME("now", "-1 hour"), DATETIME("now")),
            (192, 1092, DATETIME("now", "-2 days"), NULL);
        
        INSERT INTO agents VALUES
            ("a0", "John Bond", "pw0"),
            ("a1", "James Bond", "pw1"),
            ("a2", "Your Mom", "pw2"),
            ("a3", "Michael Jackson", "pw3");        
    """) 
    # this executescript POPULATES data into our tables; the purpose is to add test data.
    conn.commit()
    return


# Shardul
def set_up_delivery():
    return


#Shardul
def update_delivery():
    return


# Ceegan
def add_to_stock():
    return


# Shardul
def search_for_product():
    return


# Ceegan
def place_an_order():
    return


# Ceegan
def list_orders():
    return


def main():
    
    # establishes DB
    path = "./mp1.db"
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;') # turns on FKs for the DB for the rest of the connection
    conn.commit()
    user_flag = 0
    basket = [] # basket, i.e shopping cart

    # Following two lines creates and populates data into the database. Remove before submitting (I think. FIXME)
    add_tables(conn)
    test_data(conn)

    first_time_resp = input("Welcome! Please choose (press 1, 2, or 3) one of the following options:\n1. Login\n2. Register  \n3. Quit"
                            "\n\n> ")
    
    while first_time_resp != '1' and first_time_resp != '2' and first_time_resp != '3':
        first_time_resp = input("> ")
        
    if first_time_resp == '1':
        user_flag = login(conn, input("\nUsername: "), input("Password: "))
        while user_flag == 0:
            print("You entered your password or username incorrectly. Please try again.")
            user_flag = login(conn, input("\nUsername: "), input("Password: "))

    elif first_time_resp == '2':

        # note all agents are assumed to be registered, so there cannot be a new account being made for agents
        # making new account for customer:
        print("\nPlease fill out the following required entries to sign up as a customer\n")
        new_cid = input("Provide a customer ID: ")
        new_name = input("Enter your full name: ")
        new_addr = input("Enter your address: ")
        new_pwd = input("Enter a password for your account: ")

        while cust_sign_up(conn, new_cid, new_name, new_addr, new_pwd) == 0:
            print("\nThe given ID is NOT unique.")
            new_cid = input("Please enter a unique customer ID: \n")

        print("\nSuccess! You have signed up.\n")

        # Is it ok if the user is automatically logged in after sign up?
        user_flag = login(conn, new_cid, new_pwd)

    else:
        conn.close()
        return

    # user_flag is the same as security level. That is:
    # if user_flag = 1, user is an agent
    # if user_flag = 2, user is a customer
    # if user_flag = 0, user is neither (should be impossible at this point according to our code)
         
    print("Security lvl: ", user_flag, "\n")
    
    if user_flag == 1:
        # agent commands
        action = input("Welcome to the agent interface. Please choose (press 1, 2, 3, or 4) from one of the following options:\n"
                       "1. Set up a delivery\n2. Update a delivery\n3. Add to stock\n4. Quit\n\n> ")
        while action != "1" and action != "2" and action != "3" and action != "4":
            action = input("> ")

        if action == 1:
            set_up_delivery()
        elif action == 2:
            update_delivery()
        elif action == 3:
            add_to_stock()

    else:
        action = input("Welcome to the customer interface. Please choose (press 1, 2, 3 or 4) from one of the following options:\n"
                       "1. Search Products\n2. Place an order\n3. List orders\n4. Quit\n\n> ")

        while action != "1" and action != "2" and action != "3" and action != "4":
            action = input("> ")

        if action == 1:
            search_for_product()
        elif action == 2:
            place_an_order()
        elif action == 3:
            list_orders()

    conn.close()

if __name__ == '__main__':
    main()
    
# Questions to ask prof:
    # Is it ok if the user is automatically logged in after sign up?
    # What exactly is the prof looking for in the "exit the program" option?
    # Is the test gonna involve hard testing and trying to break EVERYTHING? Like, for example: first_time_user saying
    # no, hes not one when in reality he is, which causes an infinite loop in the incorrect 'user/pass' section
    # Is the "y/n" way fine?
    # Do we need a separate login option for agents and customers?
    # Do we remove our test data in the end before submitting? How will they add the data?
    # Do we need a quit message?

# Things to add: 
    # Bucket list
    # Agent commands
    # Customer commands
    # More Test data
    # Option to exit anytime
