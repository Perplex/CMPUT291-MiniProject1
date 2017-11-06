# Go to end of code for things to add/questions

import sqlite3
import os.path

def login(conn, user, passw):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agents WHERE aid=? and pwd=?;", (user, passw))
    row = cursor.fetchone()
    conn.commit()

    if row is not None:
        return 1 # user is an agent

    cursor.execute("SELECT * FROM customers WHERE cid=? and pwd=?;", (user, passw))
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
            ("bak10", "Bread, Brown, Sliced", "ea", "bak"),
            ("bak11", "Bread, Bread, Bread, Bread, Bread", "ea", "bak"),
            ("bak12", "Cheese Bread", "ea", "bak"),
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

            (0, "bak0", 0, 3.29),
            (0, "bak10", 25, 4.99),
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
            (191, 1030, DATETIME("now"), NULL),
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


def generate_UTN(conn):
    # generation of unique tracking number
    # function returns a UTN (Unique Tracking Number)
    c = conn.cursor()
    c.execute("""SELECT d1.trackingno FROM deliveries d1 ORDER BY trackingno DESC LIMIT 1;""")
    unique_TN = c.fetchone()[0]

    if unique_TN is None:
        unique_TN = 0
    
    return unique_TN + 1


# Shardul
def set_up_delivery(conn):
    # new delivery
    
    c = conn.cursor()
    
    # generation of unique tracking number
    unique_TN = generate_UTN(conn)

    add_oid = 0 # int
    add_put = "" # string

    while True:
        order_resp = input("Would you like to add (more) orders to the new delivery? (y/n): ")
        while order_resp != 'y' and order_resp != 'n':
            order_resp = input("Invalid response, please try again (y/n): ")
        
        if order_resp == 'y':
            # FIXME add error checking for orderid; if agent puts an OID not in the DB
            add_oid = int(input("Please enter the order ID for the order you want to add to the delivery: "))
            
            PUT_resp = input("Would you like to add a pick up time for this order? (y/n): ")
            while PUT_resp != 'y' and PUT_resp != 'n':
                PUT_resp = input("Invalid response, please try again (y/n): ")
                                
            if PUT_resp == 'y':
                print("Insert the date in a 'YYYY-MM-DD HH:MM:SS' format:\n ")
                year = input("Insert YYYY: ")
                month = input("Insert MM: ")
                day = input("Insert DD: ")
                hour = input("Insert HH: ")
                minute = input("Insert MM: ")
                second = input("Insert SS: " )
                
                add_put = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second # this is the required format to store datetime in SQLite3 ; it is the format SQLite stores datetimes in. i.e. time is stored in the YYYY-MM-DD HH:MM:SS format in SQLite3
                
            if add_put == "":
                 c.execute("""INSERT INTO deliveries VALUES (?, ?, ?, ?);""", (unique_TN, add_oid, None, None))
                 conn.commit()
            else:
                c.execute("""INSERT INTO deliveries VALUES (?, ?, ?, ?);""", (unique_TN, add_oid, add_put, None)) 
                conn.commit()
                               
            print("Successfully added order to the delivery")      
                      
        else:
            break        
    
    # FIXME: for testing purposes
    c.execute("SELECT* FROM deliveries;")
    rows = c.fetchall()
    print(rows)
    
    return


# Shardul
def update_delivery(conn):
    # change info of existing delivery
    # assumes if no order left in a delivery ,the delivery does not exist. Is this right? FIXME
    #FIXME add error checking for orderid; if agent puts an OID not in the DB
    
    c = conn.cursor()
    
    while True:
        t_no = input("Please enter the tracking number of the delivery you want to update: ")
        c.execute("SELECT * FROM deliveries WHERE trackingNo=?;", (t_no,))
        row = c.fetchone()
    
        while row == None:
            print("That tracking number does not exist in the system. Try again: ")
            t_no = input("Please enter the tracking number of the delivery you want to update: ")
            c.execute("SELECT * FROM deliveries WHERE trackingNo=?;", (t_no,))
            row = c.fetchone()
        
        c.execute("SELECT * FROM deliveries WHERE trackingNo=?;", (t_no,))
        rows = c.fetchall()    
    
        print("Here are the details of the delivery you selected: \n")
    
        for each in rows:
            print("Tracking number: ", each[0], "\nOrder ID: ", each[1], "\nPick Up Time: ", each[2], "\nDrop Off Time: ", each[3], "\n")
        
        update_resp = input("\nWould you like to pick up an order? (y/n)?: ") 
        while update_resp != 'y' and update_resp != 'n':
            update_resp = input("Invalid response, please try again (y/n): ") 
        
        if update_resp == 'y':
            oid = input("Please enter the order ID of the order you want to pick up:  ")
        
            #FIXME add error checking for orderid; if agent puts an OID not in the DB
        
            c.execute("SELECT * FROM deliveries WHERE trackingNo=? AND oid=?;", (t_no, oid))
            row = c.fetchone()
        
            print("Following order picked up: \n")
            print("Tracking number: ", row[0], "\nOrder ID: ", row[1], "\nPick Up Time: ", row[2], "\nDrop Off Time: ", row[3])
        
            PUT_resp = input("Would you like to update the pick up time of the order (y/n)?: ")
            while PUT_resp != 'y' and PUT_resp != 'n':
                PUT_resp = input("Invalid response, please try again (y/n): ")
            
            if PUT_resp == 'y':
                new_PUT = input("Enter the new pick up time of the order in a 'YYYY-MM-DD HH:MM:SS' format: ")
                c.execute(""" UPDATE deliveries SET pickUpTime=? WHERE trackingNo=? AND oid=?;""", (new_PUT, t_no, oid))
                conn.commit()
                # test FIXME
                print("Pick up time updated to:", new_PUT)
                    
            DOT_resp = input("Would you like to update the drop off time of the order (y/n)?: ")
            while DOT_resp != 'y' and DOT_resp != 'n':
                DOT_resp = input("Invalid response, please try again (y/n): ")
        
            if DOT_resp == 'y':
                new_DOT = input("Enter the new drop off time of the order in a 'YYYY-MM-DD HH:MM:SS' format: ")
                c.execute(""" UPDATE deliveries SET dropOffTime=? WHERE trackingNo=? AND oid=?;""", (new_DOT, t_no, oid))
                conn.commit()
                # test FIXME
                print("Drop off time updated to:", new_DOT)   
               
        update_resp = input("\nWould you like to remove an order from the delivery? (y/n)?: ") 
        while update_resp != 'y' and update_resp != 'n':
            update_resp = input("Invalid response, please try again (y/n): ")  
        
        if update_resp == 'y':
            oid = input("Please enter the order ID of the order you want to remove from the delivery:  ")
            #FIXME add error checking for orderid; if agent puts an OID not in the DB
            
            c.execute("""DELETE FROM deliveries WHERE trackingNo=? AND oid=?;""", (t_no, oid))
            conn.commit()
            print("Order deleted succesfully")
            
        exit_resp = input("Please choose from one of the following options:\n" "1. Pick a new delivery to update. \n2. Exit update_delivery interface (1/2) \n\n")
        if exit_resp == '2':
            break             
    return


# Ceegan
def add_to_stock(conn):
    while True:
        pid = input("\nPlease input the product ID for the product you would like to change: ")
        sid = input("Now input the store ID for this product: ")

        c = conn.cursor()

        c.execute('''select qty from carries where sid=? and pid=?''', (sid, pid))
        qty = c.fetchone()

        if qty is None:
            print("Sorry but the product and store IDs entered do not match. Please try again")
        else:
            amount = input("What is the amount of products to add to this store?: ")
            choice = input("Would you like to change the unit price as well?(y/n): ")

            while choice != 'y' and choice != 'n':
                choice = input("Invalid response please try again (y/n): ")

            qty = qty[0]
            if choice == 'y':
                uprice = input("Input the new unit price: ")
                c.execute('''update carries set qty = ?, uprice = ? where sid=? and pid = ?''', (int(amount)+qty, uprice, sid,
                                                                                                 pid))
            else:
                c.execute('''update carries set qty = ? where sid=? and pid = ?''', (int(amount)+qty, sid, pid))

            conn.commit()

            for row in c.execute('''select * from carries where sid =? and pid=?''', (sid, pid)):
                print(row)

            choice = input("Would you like to update another items stock? (y/n): ")
            while choice != 'y' and choice != 'n':
                choice = input("Invalid response, please try again (y/n): ")

            if choice == 'n':
                break

    return


# Ceegan
def search_for_product(conn):
    c = conn.cursor()

    # Get keywords to search for
    keyword_string = input("Please enter one or more keywords to search for products, with a space separating each (e.g. egg yolk fresh): ")
    keyword_list = keyword_string.split()

    # init variables
    matches = {}
    baseket = []

    # search for keyword matches
    for keyword in keyword_list:
        row = c.execute('''select pid, name, unit, count(sid), count(case when qty > 0 then 1 end), MIN(uprice)
                           from products
                           left join carries using (pid)
                           where name like ?
                           group by pid''', ('%' + keyword + '%',))

        # Keep track of amount of matches per product
        for item in row.fetchall():
            if item in matches:
                matches[item] += 1
            else:
                matches[item] = 1

    print("PID|product name|unit|number of stores that carry|number of stores with in stock| min price of all stores")

    while True:
        # print products five at a time
        if len(matches) < 5:
            size = len(matches)
        else:
            size = 5
        for x in range(size):
            key = max(matches, key=matches.get)
            print(key)
            matches.pop(key)

        choice = input("\nPlease select one of the following:\n1. See next five entries\n2. More details of a product\n"
                       "3. Add an item to my basket\n4. Quit\n\n> ")

        if choice == '2':
            choice = input("Please input the product ID of the product that you would like to know more about: ")

            # Getting more detials for desired product
            row = c.execute('''select carries.pid, products.name, unit, cat, stores.name, uprice, qty
                               from products, stores, carries
                               where products.pid = ? and products.pid = carries.pid and carries.sid = stores.sid
                               order by qty=0, uprice''',
                            (choice,))

            for item in row.fetchall():
                print(item)

            # Checking if user wants to add a product to basket
            choice = input("\nWould you like to add an item to your basket?(y/n) ")
            if choice == 'y':
                choice = '3'

        # Add item to basket
        if choice == '3':
            pid = input("\nPlease input the product ID of the product you would like to add to your basket: ")
            qty = input("How many would you like to add? ")

            # Error check qty
            while not qty.isdigit() and int(qty) <= 0:
                qty = input("Invalid qty, please try again: ")

            # fetch all stores that carry desired product
            row = c.execute('''select name, sid from carries left join stores using(sid) where pid = ?''', (pid,))
            row = row.fetchall()

            for x in range(len(row)):
                print(str(x+1) + '. ' + row[x][0])

            choice = input("\nPlease choose the store you would like to order from: ")

            sid = row[int(choice)-1][1]

            # Get uprice for product from store
            row = c.execute('''select uprice from carries where pid = ? and sid = ?''', (pid, sid))

            # Add item to basket
            baseket.append([pid, int(sid), int(qty), float(row.fetchone()[0])])

        elif choice == '4':
            break

    return baseket


# Ceegan
def place_an_order(username, basket, conn):
    c = conn.cursor()

    # get most recent order ID
    c.execute('''select * from orders order by oid DESC limit 1''')
    maxOid = c.fetchone()[0]

    # If no orders have been made yet
    if maxOid is None:
        maxOid = 0

    # Get user address
    c.execute('''select address from customers where cid = ?''', (username,))
    address = c.fetchone()[0]

    # Insert new order into orders
    c.execute('''insert into orders values (?, ?, DATE("now"), ?)''', (maxOid + 1, username, address))
    conn.commit()

    # for item in basket insert into olines
    for item in basket:
        c.execute('''select qty
                     from carries
                     where pid=? and sid=?''', (item[0], item[1]))

        # If the quantity is greater then the store carries
        row = c.fetchone()
        if item[2] > row[0]:

            # Input new qty or delete
            choice = input("\nThe quantity for " + item[0] + " is greater than what your selected store carries.\nWould"
                                                             " you like change the qty (c) or delete the item (d)?: ")
            while choice != "c" and choice != "d":
                choice = "Invalid response, please try again: "

            if choice == 'd':
                basket = [x for x in basket if not item]
            elif choice == 'c':
                while item[2] > row[0]:
                    choice = input("Please input the new quantity, new quantity must be equal to or less then " +
                                   str(row[0]) + ": ")

                    while not choice.isdigit():
                        choice = input("Please input an integer: ")

                    item[2] = int(choice)

                # Insert changed qty item into olines
                c.execute('''insert into olines values (?, ?, ?, ?, ?)''', (maxOid + 1, item[1], item[0], item[2],
                                                                            item[3]))
                conn.commit()
        else:
            # Insert item into olines
            c.execute('''insert into olines values (?, ?, ?, ?, ?)''', (maxOid + 1, item[1], item[0], item[2],
                                                                        item[3]))
            conn.commit()

    print("Items have been ordered!")
    return


# Ceegan
def list_orders(cid, conn):
    c = conn.cursor()

    # Get all orders
    c.execute('''Select oid, odate, sum(qty), round(sum(uprice*qty), 2)
                 from orders
                 left join olines using(oid)
                 where cid = ?
                 group by oid, odate
                 order by date(odate) desc''', (cid,))

    # Continue till user wants to go back
    while True:

        # Print five orders
        rows = c.fetchmany(5)
        for stuff in rows:
            print(stuff)

        # Get user input then error check
        choice = input("\nPlease select one of the following:\n1. Next five orders\n2. More info about an order\n"
                       "3. Go Back"
                       "\n\n> ")
        while choice != "1" and choice != "2" and choice != "3":
            choice = input("Please select one of the following:\n1. Next five orders\n2. More info about an order\n"
                           "3. Go Back\n\n> ")
        if choice == "3":
            break
        elif choice == "2":
            # Getting more details

            choice = input("Please input the order ID that you would like to now more about: ")
            d = conn.cursor()
            d.execute('''select trackingno, pickUpTime, dropOffTime, address
                         from orders
                         left join deliveries using (oid)
                         left join olines using (oid)
                         where oid =?''', (choice, ))

            row = d.fetchone()

            # Order ID is valid
            if row:
                print(row)

                for lines in d.execute('''select sid, stores.name, pid, products.name, qty, unit, uprice
                             from olines
                             left join stores using (sid)
                             left JOIN products using (pid)
                             where oid = ?''', (choice,)):
                    print(lines)
            else:
                print("Invalid order ID")

    return


def main():
    path = ""
    path = input("Welcome! Please input the path of the DB: ")

    while not os.path.exists(path):
        path = input("Unable to find DB, please try again: ")


    # establishes DB
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;') # turns on FKs for the DB for the rest of the connection
    conn.commit()

    user_flag = 0

    # [pid, sid, qty, uprice] per element in basket
    basket = []
    username = ''

    # Following two lines creates and populates data into the database. Remove before submitting (I think. FIXME)
    add_tables(conn)
    test_data(conn)

    first_time_resp = input("\nPlease choose (press 1, 2, or 3) one of the following options:\n1. Login\n2. Register  "
                            "\n3. Quit\n\n> ")
    
    while first_time_resp != '1' and first_time_resp != '2' and first_time_resp != '3':
        first_time_resp = input("> ")
        
    if first_time_resp == '1':
        username = input("\nUsername: ")
        user_flag = login(conn, username, input("Password: "))
        while user_flag == 0:
            print("You entered your password or username incorrectly. Please try again.")
            username = input("\nUsername: ")
            user_flag = login(conn, username, input("Password: "))

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
         
    print("Security lvl: ", user_flag)
    
    if user_flag == 1:
        # agent commands
        while True:
            action = input("\nWelcome to the agent interface. Please choose from one of the following options:\n"
                           "1. Set up a delivery\n2. Update a delivery\n3. Add to stock\n4. Quit\n\n> ")
            while action != "1" and action != "2" and action != "3" and action != "4":
                action = input("> ")

            if action == "1":
                set_up_delivery(conn)
            elif action == "2":
                update_delivery(conn)
            elif action == "3":
                add_to_stock(conn)
            elif action == '4':
                break

    else:
        while True:
            action = input("\nWelcome to the customer interface. Please choose from one of the following options:\n"
                           "1. Search Products\n2. Place an order\n3. List orders\n4. Quit\n\n> ")

            while action != "1" and action != "2" and action != "3" and action != "4":
                action = input("> ")

            if action == "1":
                basket = search_for_product(conn)
            elif action == "2":
                #basket = [["bak0", 0, 15, 3.29], ["bak1", 1, 5, 5.99], ["bak2", 1, 24, 5.99]]
                place_an_order(username, basket, conn)
                basket = []
            elif action == "3":
                list_orders(username, conn)
            elif action == "4":
                break

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

