"""

This SQL Database stores employee name, title, pay, contact details, and department. 

"""

import sqlite3

def analyze_object(object):
    print(f"Object: {type(object)}")
    for name in dir(object):
        if not name.startswith("__"):
            attribute = getattr(object,name)    
            if callable(attribute):
                print(f"Function: {name}")
            else:
                print(f"{name} = {attribute}")
    print()

# Connect to the database
connection = sqlite3.connect('employeedatabase.db')
cursor = connection.cursor()

# Create table (if it does not already exist)
cursor.execute("CREATE TABLE IF NOT EXISTS employees (name TEXT, title TEXT, pay REAL, contact TEXT, department TEXT)")
       
def get_name(cursor):
    cursor.execute("SELECT name FROM employees")
    results = cursor.fetchall()
    if len(results) == 0:
        print("No names in database")
        return None
    for i in range(len(results)):
        print(f"{i+1} - {results[i][0]}")
    choice = 0
    while choice < 1 or choice > len(results):
        choice = int(input("Name ID: "))
    return results[choice-1][0]


choice = None
while choice != "5":
    print("1) Display Employees")
    print("2) Add Employee")
    print("3) Update Employee Pay")
    print("4) Delete Employee")
    print("5) Quit")
    choice = input("> ")
    print()
    if choice == "1":
        # Display Employees
        result = cursor.execute("SELECT * FROM employees ORDER BY pay DESC")
        # analyze_object(result)
        print("{:>10}  {:>10}  {:>10}  {:>10}  {:>10}".format("Name", "Title", "Pay", "Contact", "Department"))
        for record in cursor.fetchall():
            print("{:>10}  {:>10}  {:>10}  {:>10}  {:>10}".format(record[0], record[1], record[2], record[3], record[4]))
    elif choice == "2":
        # Add New Employee
        try:
            name = input("Name: ")
            title = input("Title: ")
            pay = float(input("Pay: "))
            contact = input("Contact Number: ")
            dept = input("Department: ")
            values = (name, title, pay, contact, dept)
            cursor.execute("INSERT INTO employees VALUES (?,?,?,?,?)", values)
            connection.commit()
        except ValueError:
            print("Unable to process. Try again.")
    elif choice == "3":
        # Update Employee Pay
        try:
            name = input("Name: ")
            pay = float(input("Pay: "))
            values = (pay, name) # Make sure order is correct
            cursor.execute("UPDATE employees SET pay = ? WHERE name = ?", values)
            connection.commit()
            # analyze_object(result)
            if cursor.rowcount == 0:
                print("Invalid name!")
        except ValueError:
            print("Invalid pay!")
    elif choice == "4":
        # Delete employee
        name = get_name(cursor)
        if name == None:
            continue
        values = (name, )
        cursor.execute("DELETE FROM employees WHERE name = ?", values)
        connection.commit()
    print()

# Close the database connection before exiting
connection.close()