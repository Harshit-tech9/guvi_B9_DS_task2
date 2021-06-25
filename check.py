from codecs import register
import mysql.connector
import re


con = mysql.connector.connect(host="localhost", user="root", password="123456789", database="pythonlogin")
cur = con.cursor(prepared = True)
def register():
    username = input("username: ")
    email = input("email id: ")
    password = input("password: ")
    password1 = input("password: ")

    cur.execute("SELECT * FROM accounts WHERE username = '"+username+"'")
    account = cur.fetchone()
    if account:
        print('Account already exists !')
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        print('Invalid email address !')
    elif not re.match(r'[A-Za-z0-9]+', username):
        print('Username must contain only characters and numbers !')
    elif not password == password1:
        print('password does not matched! Enter the password again')
    elif not username or not password or not email:
        print('Please fill out the form !')
    else:
        cur.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email,))
        con.commit()
        print('You have successfully registered !')

def login():
    username = input("Name: ")
    password = input("password = ")

    cur.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
    account = cur.fetchone()
    con.commit()
    if account:
        print ("Log in successfull")
    else:
        print("log in unsuccessfull")
        return 1


def forgot_password():
    name = input("Enter your username : ").lower()
    try:
        password = cur.execute("SELECT password FROM accounts WHERE username = '"+name+"'").lower()
        if (password):
            print("Your password : '"+password+"'")
            con.commit()
        else:
            print("Username Not Found! \n Please Register Yourself..")
            register()
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)

    finally:
        if con.is_connected():
            con.close()
            cur.close()
            print("MySQL connection is closed")


"""
def logout():
    logout = ("Do you wish to logout yes/no?")

    if logout == yes:
        exit()

    else:
        os.system("shutdown -1")
"""

while(True):
    account = input("Do you have an account? \n(Please enter yes or no)").lower()
    if account == 'yes':
        a = login()
        if a == 1:
            op = input(("Forgot Password? : \n(Please enter yes or no")).lower()
            if op == 'yes':
                forgot_password()
            else:
                login()
        else:
            print(a)

        pass
    elif account == 'no':
        print ("please register yourself!")
        register()
        pass

    else:
        print("Thank you")
        break
