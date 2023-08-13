# Connecting to database
def createConnect():
    conn=sq.connect("D:\\python\\contactmgmt.db")
    cur=conn.cursor()
    conn.commit()
    return conn

# Creating table
def createTable(conn):
    cur=conn.cursor()
    cur.execute("CREATE TABLE CONTACT(fname text, laname text, contact numeric, email text, city text);")
    conn.commit()

# Creating Log table
def createLog(conn):
    cur=conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS CONTACT_log
        (
        fname text,
        lname text,
        contact integer,
        datetime text,
        operation_performed text
        );""")             #creating log table
    conn.commit()

# Creating Triggers for Log table
def logTrigger(conn):
    cur=conn.cursor()
    cur.execute("""CREATE TRIGGER IF NOT EXISTS insertLogTrigger
                        after insert
                        on contact
                        BEGIN
                            INSERT INTO CONTACT_log
                            VALUES(new.fname,new.laname,new.contact,datetime('now','localtime'),'INSERT');
                        END;""")
    cur.execute("""CREATE TRIGGER IF NOT EXISTS deleteLogTrigger
                        after delete 
                        on contact
                        BEGIN
                            INSERT INTO CONTACT_log
                            VALUES(old.fname,old.laname,old.contact,datetime('now','localtime'),'DELETE');
                        END;""")
    cur.execute("""CREATE TRIGGER IF NOT EXISTS updateLogTrigger
                        after update
                        on contact
                        BEGIN
                            INSERT INTO CONTACT_log
                            VALUES(new.fname,new.laname,new.contact,datetime('now','localtime'),'After UPDATE');
                            INSERT INTO CONTACT_log
                            VALUES(old.fname,old.laname,old.contact,datetime('now','localtime'),'Before UPDATE');
                        END;""")
    conn.commit()

# Creating Validating Trigger
def createTrigger(conn):
    cur=conn.cursor()
    conn.execute("""CREATE TRIGGER validate_field 
    BEFORE INSERT
    ON CONTACT
    BEGIN
    SELECT
    CASE
    WHEN new.email NOT LIKE '%@%.%' THEN
        RAISE(ABORT,'Please enter email in correct format')
    WHEN length(new.contact)<10 THEN
        RAISE(ABORT,'Ivalid Contact Number. Please enter correct number.')\
    END;
    END;""")            #validating email format and contact number
    conn.commit()

# Inserting records
def insertRecords(conn):
    cur=conn.cursor()
    fname=input("\n\nEnter first name: ")
    lname=input("Enter last name: ")
    contact=int(input("Enter contact: "))
    email=input("Enter email:")
    city=input("Enter city: ")
    L=[fname,lname,contact,email,city]
    conn.execute("INSERT INTO CONTACT VALUES(?,?,?,?,?);",L)
    print('\n\nContact inserted sucessfully.\n')
    conn.commit()

# Updating Records
def updateContacts(conn):
    cur=conn.cursor()
    name_search=input("\n\nEnter their First name: ")
    new_contact=input("Enter New Contact No :")
    cur.execute(f"update CONTACT set contact='{new_contact}' where fname='{name_search}'")
    print("\n\nContact updated successfully.\n")
    conn.commit()

# Deleting Records
def deleteContacts(conn):
    cur=conn.cursor()
    name_search=input("\n\nEnter their First Name: ")
    cur.execute(f"delete from CONTACT where fname='{name_search}'")
    print("\n\nContact deleted successfully.\n")
    conn.commit()

# Searching Records
def searchContacts(conn):
    cur=conn.cursor()
    name_search=input("\n\nEnter their First Name: ")
    cur.execute(f"select * from CONTACT where fname='{name_search}'")
    records=cur.fetchall()
    print('\n____________________________________________________________________________________')
    print('Fname\tLaname\tContact\t\tEmail\t\t\tCity')
    print('______________________________________________________________________________________')
    for rows in records:
        print('{}\t{}\t{}\t{}\t{}'.format(rows[0],rows[1],rows[2],rows[3],rows[4]))       #all records will be shown
    print('\n\nThis are all available records\n')
    conn.commit()

# Viewing All Records
def viewRecords(conn):
    cur=conn.cursor()
    cur.execute('select * from CONTACT')
    records=cur.fetchall()
    print('\n____________________________________________________________________________________')
    print('Fname\tLaname\tContact\t\tEmail\t\t\tCity')
    print('______________________________________________________________________________________')
    for rows in records:
        print('{}\t{}\t{}\t{}\t{}'.format(rows[0],rows[1],rows[2],rows[3],rows[4]))       #all records will be shown
    print('\n\nThis are all available records')
    conn.commit()

# Operating Function
def operationFunct():
    conn=createConnect()
    createTable(conn)
    createLog(conn)
    createTrigger(conn)
    logTrigger(conn)
    choice=1
    while choice!=0:
        print('\n-------------------------------------------------------------------------------------------------')
        print('1- Insert contacts')
        print('2- Update contacts')
        print('3- Delete contacts')
        print('4- Search contacts')
        print('5- View all records')
        print('0- Exit the program')
        choice=int(input('\nEnter your choice: '))      #choosing operations
        if choice==1:
            insertRecords(conn)       #directly calling function
        elif choice==2:
            updateContacts(conn)       #directly calling function
        elif choice==3:
            deleteContacts(conn)       #directly calling function
        elif choice==4:
            searchContacts(conn)       #directly calling function
        elif choice==5:
            viewRecords(conn)       #directly calling function
    conn.close()

import sqlite3 as sq     #importing sqlite3 module
operationFunct()       #directing calling function
