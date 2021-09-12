import string
import secrets
import sqlite3 as sql


# --------------------- Database -----------------------
conn = sql.connect("User_Database.db")
# Creating a cursor
c = conn.cursor()

# Create a table
c.execute("""CREATE TABLE IF NOT EXISTS Users(
                    Name text, 
                    Website text,
                    Email text, 
                    Password blob
                    )""")
conn.commit()
# --------------------------------------------------------

# ----------- Password Generator ------------- #


def create_password(limit, special='N'):
    if special.lower() == "y":
        password = "".join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for x in range(limit))
        return password
    elif special.lower() == "n":
        password = "".join(secrets.choice(string.ascii_letters + string.digits) for x in range(limit))
        return password



# ----- The Function is used to enter a new user with generation of password --------#


def insert_user(name, mail, site, password):
    # First look for if the same user is trying to input password for same email address and same site

    c.execute(" SELECT * FROM Users WHERE Name = ? AND Email = ? AND Website = ? ", (name, mail, site, ))
    verify = c.fetchall()
    conn.commit()

    if len(verify) != 0:
        return print(" User {} with same site and mail exists already. To update select update on program run".format(name))
    else:
        with conn:
            c.execute("INSERT INTO Users VALUES (?, ?, ?, ?)", (name, site, mail, password))  # Inserting into database
            return print("\n ==== Inserted in to the database successfully ===")

# ------- The function simply stores user defined password for later usage ------ #


def store_user(name):

    site = str(input("Input the site you want to store password for: "))
    mail = input("Input mail address: ")

    c.execute(" SELECT * FROM Users WHERE Name = ? AND Email = ? AND Website = ? ", (name, mail, site,))
    verify = c.fetchall()
    conn.commit()

    if len(verify) != 0:
        return print("User {} with same site and mail exists already. To update select update on program run".format(name))

    else:
        password = str(input("Enter the password you want to store for later usage: "))

        print("The password {} is going to be stored in database for {} site and {} mail".format(password, site, mail))

        c.execute(" INSERT INTO Users VALUES( ?, ?, ?, ?)", (name, site, mail, password,))
        conn.commit()
        print("Credentials Stored in the database Successfully")

# --- The function is used to search for the valid entries


def search_user(name):

    c.execute(" SELECT * FROM Users WHERE Name = ?", (name,))
    verify = c.fetchall()

    if len(verify) != 0:
        with conn:
            print("ID       Name           Website             Mail                   Password ")
            print("_______________________________________________________________________________ ")
            for row in c.execute(" SELECT rowid, * FROM Users WHERE Name = ?", (name,)):
                print(" {}      {}      {}      {}      {}\n".format(row[0], row[1], row[2], row[3], row[4]))
    else:
        return print("No entries such that exists")


# ---- The function is used to update a remaining user --- #


def update_user(name):

    search_user(name)
    update = input("Enter the ID you are willing to update: ")

    choice = input("Do you want to generate a password or store one of your own. Type 'Create' or 'Store' :")

    if choice.lower() == "create":
        limit = input("Enter the length: ")
        special = input("Special characters supported? Y or N")

        password = create_password(limit, special)

        c.execute("UPDATE Users SET Password = ? WHERE Name=? AND rowid=?", (password, name, update, ))
        conn.commit()
        return print("Your new password is {}".format(password))
    elif choice.lower() == "store":
        new = input("Enter the password you desire to save: ")
        print("Your new password is {}".format(new))

        c.execute("UPDATE Users SET Password = ? WHERE Name=? AND rowid=?", (new, name, update, ))
        conn.commit()

# -- The function is used to delete a user -- #


def delete_user(name):

    c.execute(" SELECT rowid, * FROM Users WHERE Name = ?", (name,))  # Verifying if any entries with the name exists

    all = c.fetchall()

    if len(all) == 0:
        print("There is no such entries, Please try again with accurate entries")

    else:
        search_user(name)
        delete = input("Enter the Entry Id you want to delete: ")

        with conn:
            c.execute("DELETE FROM Users WHERE rowid=? AND Name=?", (delete, name, ))
            conn.commit()
            return print("Successfully Deleted the entry")


# -------------------------- Input User Data -----------------------------#


print("        =============  Welcome to Achilles Password Manager ============= \n")
print("___________________________________________________________________________________________________ ")
print("""You can create & store password for your social media accounts or simply store your password 
         Search for the password you stored, update and delete the records also """)
print("___________________________________________________________________________________________________ ")


choice = str(input("       ======> Type Create, Store, Update, Search or Delete as you wish. <=======  \n"))


if choice.lower() == "create":
    name = str(input("Enter your name please: "))
    site = str(input("Input the site you want to generate password for: "))
    mail = input("Input mail address: ")
    special = str(input("Does the site support special characters? Y or N :"))

    limit = int(input("Input the character limit: "))

    password = create_password(limit, special)  # Creates the password
    print("Your password is {}".format(password))

    insert_user(name, site, mail, password)

elif choice.lower() == "store":

    nam_store = str(input("Enter your name please: "))

    store_user(nam_store)

elif choice.lower() == "update":

    nam_up = input("Enter your name: ")

    update_user(nam_up)


elif choice.lower() == "search":

    nam_search = str(input("Enter your name :"))

    print("Here is what we found \n")

    search_user(nam_search)

elif choice.lower() == "delete":

    nam_delete = input("Enter your name: ")

    delete_user(nam_delete)
    conn.commit()

conn.close()
