import sqlite3

#connection to database
data = sqlite3.connect("gymMembers.csv")
d = data.cursor()

#Main function
def main():
    keepGoing = True
    while keepGoing:
        result = menu()
        if result == "A":
            keepGoing = False
        elif result == "012345":
            build()
        elif result == "B":
            createMember()
        elif result == "C":
            reportAll()
        elif result == "D":
            updateMember()
        elif result == "E":
            deleteMember()
        elif result == "F":
            searchMember()
        else:
            print("Error: Not a proper response. Please try again.")
    #Close connection to database
    d.close()

#Defines menu, uses main function
def menu():
    print("""
    A) Exit
    B) Create new member
    C) Report all records
    D) Update member record
    E) Delete member record
    F) Search for member(s)
    012345) Build default members
    """)
    result = input("What would you like to do? ")
    result = result.upper()
    return result

def build():
    d.execute("DROP TABLE IF EXISTS members")
    sql = """
    CREATE TABLE members (
    id INTEGER PRIMARY KEY,
    Name VARCHAR(20),
    DOB VARCHAR(13),
    Phone VARCHAR(13),
    Status VARCHAR(13)
    )"""
    d.execute(sql)

  #insert records into the table
    d.execute("INSERT INTO members VALUES (null, ?, ?, ?, ?)",
            ('Arnold Stewarts', '11/01/1942', '(812)281-2401', 'Active'))
    d.execute("INSERT INTO members VALUES (null, ?, ?, ?, ?)",
            ('John Bogus', '01/02/03', '(098)-765-4321', 'Terminated'))
    d.execute("INSERT INTO members VALUES (null, ?, ?, ?, ?)",
            ('Newborn Baby', '12/12/2019', '(123)456-7890', 'On-Hold'))

  # need to commit to save changes
    data.commit()

#Creates record, asks for information for new record
def createMember():
    name = input("First and Last name: ")
    dob = input("Date of Birth: ")
    phone = input("Phone Number: ")
    status = input("Membership Status: ")

    d.execute("INSERT INTO members VALUES(null, ?, ?, ?, ?)",
    (name, dob, phone, status))
    data.commit()

def reportAll():
    #Reports every record in the database

    #views results
    result = d.execute("SELECT * FROM members")

    memberRec = [description[0] for description in result.description]

    for member in result:
        num = 0
        for field in member:
            print ("{:10}: {}".format(memberRec[num], field))
            num += 1
            print("")
def updateMember():
    #Gets record, allowed values to be changed

    get = getMemberID()

    if get == 0:
        print("Cannot find. Please try again.")
    else:
        result = d.execute("SELECT * FROM members WHERE id =?",(get,))
        for row in result:
            newName = input("Name ({}): ".format(row[1]))
            if newName == '':
                newName = row[1]

            newDOB = input("Date of Birth ({}): ".format(row[2]))
            if newDOB == '':
                    newDOB = row[2]

            newPhone = input("Phone Number ({}): ".format(row[3]))
            if newPhone == '':
                    newPhone = row[3]

            newStatus = input ("Membership Status ({}): ".format(row[4]))
            if newStatus == '':
                    newStatus = row[4]

        d.execute("""UPDATE members
                    SET
                        Name = ?
                        DOB = ?
                        Phone = ?
                        Status = ?
                    WHERE
                        id = ?""",
                        (newName, newDOB, newPhone, newStatus, get))
        data.commit()

def deleteMember():
    #Gets record and deletes it.

    get = getMemberID()
    if get == 0:
        print("Not valid. Please try again.")
    else:
        result = d.execute("SELECT * FROM members WHERE id = ?", (get,))
        for row in result:
            print("Name: {}".format(row[1]))
            print("DOB: {}".format(row[2]))
            print("Phone: {}".format(row[3]))
            print("Status: {}".format(row[4]))

        confirm = input("Do you want to delete this record? (Yes/No)\n")
        confirm = confirm.upper()
        if confirm == "YES":
            d.execute("DELETE FROM members WHERE ID = ?", (get,))
            print("Member deleted.")
            data.commit()

def searchMember():
    print("""
    1) Search by name
    2) Search by Date of Birth
    3) Search by Phone

    """)
    resultMenu = input("What would you like to do? ")

    if resultMenu == "1":
        searchMember = input("Name of member: ")
        print()

        resultMenu = d.execute("SELECT * FROM members WHERE name LIKE ?",("%"+searchMember+"%",))
        for row in resultMenu:
            print("Name: {}".format(row[1]))
            print("DOB: {}".format(row[2]))
            print("Phone: {}".format(row[3]))
            print("Status: {}".format(row[4]))
            print()

    elif resultMenu == "2":
        searchMember = input("Date of Birth of Member: ")
        print()

        resultMenu = d.execute("SELECT * FROM members WHERE dob LIKE ?",("%"+searchMember+"%",))
        for row in resultMenu:
            print("Name: {}".format(row[1]))
            print("DOB: {}".format(row[2]))
            print("Phone: {}".format(row[3]))
            print("Status: {}".format(row[4]))
            print()

    elif resultMenu == "3":
        searchMember = input("Phone number of Member: ")
        print()

        resultMenu = d.execute("SELECT * FROM members WHERE phone LIKE ?",("%"+searchMember+"%",))
        for row in resultMenu:
            print("Name: {}".format(row[1]))
            print("DOB: {}".format(row[2]))
            print("Phone: {}".format(row[3]))
            print("Status: {}".format(row[4]))
            print()
    else:
        print("Not a proper response. Going back to menu.")

def getMemberID():

    result = d.execute("SELECT id, Name FROM members")

    print()
    memberIDs = []
    for row in result:
        id = row[0]
        name = row[1]
        print("{}: {}".format(id, name))

        memberIDs.append(id)

    print()
    returnMember = input("Which member number? (else enter 0 to cancel) ")

    if not returnMember.isdigit():
        print("ID must be a digit")
        returnMember = 0

    if int(returnMember) not in memberIDs:
        returnMember = 0

    return returnMember

if __name__ == "__main__":
    main()