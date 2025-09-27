import mysql.connector as vb
from datetime import datetime
vb = vb.connect(
    host="localhost",
    user="root",      
    password="Sandeep@123",
    database="sandeep" 
)
cursor = vb.cursor()
def create_account():
    name = input("Enter Name: ")
    acc_no = int(input("Enter account number[0-9]: "))
    acc_type = input("Enter account type (Savings/Current): ")
    amt = float(input("Enter Initial Deposit: "))
    pin = int(input("Set 4-digit PIN: "))
    start_date = datetime.now().date()

    query = "INSERT INTO bank_user (name, Account_no, Account_type, amt, pin, strt_date) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (name, acc_no, acc_type, amt, pin, start_date)
    cursor.execute(query, values)
    vb.commit()
    print("Account Created Successfully....!")
def record_transaction(acc_no, txt_type):
    query = "INSERT INTO bank_transaction (txt_no, Account_no, txt_type) VALUES (%s, %s, %s)"
    cursor.execute("SELECT IFNULL(MAX(txt_no),0)+1 FROM bank_transaction")
    txt_no = cursor.fetchone()[0]
    values = (txt_no, acc_no, txt_type)
    cursor.execute(query, values)
    vb.commit()
def view_balance(acc_no):
    query = "SELECT amt FROM bank_user WHERE Account_no=%s"
    cursor.execute(query, (acc_no,))
    result = cursor.fetchone()
    if result:
        print(f"Current Balance: {result[0]}")
    else:
        print("Account not found.")
def deposit(acc_no):
    amount = float(input("Enter amount to deposit: "))
    query = "UPDATE bank_user SET amt = amt + %s WHERE Account_no=%s"
    cursor.execute(query, (amount, acc_no))
    vb.commit()
    record_transaction(acc_no, f"Deposit {amount}")
    print(f"{amount} deposited successfully!")
def withdraw(acc_no):
    amount = float(input("Enter amount to withdraw: "))
    cursor.execute("SELECT amt FROM bank_user WHERE Account_no=%s", (acc_no,))
    result = cursor.fetchone()
    if result and result[0] >= amount:
        query = "UPDATE bank_user SET amt = amt - %s WHERE Account_no=%s"
        cursor.execute(query, (amount, acc_no))
        vb.commit()
        record_transaction(acc_no, f"Withdraw {amount}")
        print(f"{amount} withdrawn successfully!")
    else:
        print("Insufficient Balance.")
def view_transactions(acc_no):
    query = "SELECT txt_no, txt_type, txt_date FROM bank_transaction WHERE Account_no=%s"
    cursor.execute(query, (acc_no,))
    rows = cursor.fetchall()
    if rows:
        print("\nTransaction History:")
        for r in rows:
            print(f"{r[0]} | {r[1]} | {r[2]}")
    else:
        print("No transactions found.")
def user_login():
    acc_no = int(input("Enter Account Number: "))
    pin = int(input("Enter 4-digit PIN: "))
    query = "SELECT * FROM bank_user WHERE Account_no=%s AND pin=%s"
    cursor.execute(query, (acc_no, pin))
    result = cursor.fetchone()
    if result:
        print(f"\nWelcome, {result[0]} 👋")
        while True:
            print("\n1. View Balance\n2. Deposit\n3. Withdraw\n4. View Transactions\n5. Logout")
            choice = input("Enter choice: ")
            if choice == '1':
                view_balance(acc_no)
            elif choice == '2':
                deposit(acc_no)
            elif choice == '3':
                withdraw(acc_no)
            elif choice == '4':
                view_transactions(acc_no)
            elif choice == '5':
                break
            else:
                print("Invalid Choice.")
    else:
        print("Invalid Account Number or PIN.")
def admin_login():
    name = input("Enter Admin Name: ")
    password = input("Enter Admin Password: ")
    query = "SELECT * FROM bank_admin WHERE name=%s AND password=%s"
    cursor.execute(query, (name, password))
    result = cursor.fetchone()
    if result:
        print("\nAdmin Login Successful!")
        cursor.execute("SELECT name, Account_no, Account_type, amt, strt_date FROM bank_user")
        users = cursor.fetchall()
        print("\n-->All Customers:")
        for u in users:
            print(f"Name: {u[0]} | AccNo: {u[1]} | Type: {u[2]} | Balance: {u[3]} | Start Date: {u[4]}")
    else:
        print("Invalid Admin Credentials.")
while True:
    print("\n----->BANK MANAGEMENT SYSTEM<-------")
    print("1. Create Account")
    print("2. User Login")
    print("3. Admin Login")
    print("4. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        create_account()
    elif choice == '2':
        user_login()
    elif choice == '3':
        admin_login()
    elif choice == '4':
        print("Exiting...Thank you!")
        break
    else:
        print("Invalid Choice")



use sandeep;
#################------->user_table<------------
create table bank_user(name varchar(40) NOT NULL,Account_no int NOT NULL,Account_type varchar(30) NOT NULL,amt float Default 0,pin int NOT NULL);
alter table bank_user add constraint primary key(Account_no);
alter table bank_user add strt_date date;
select*from bank_user;
################--------->admin_Table<-----------
create table bank_admin(name varchar(30)Not null,password varchar(20));
select*from bank_admin;
insert into bank_admin values("sandeep","jack");
################--------->transcation_table<-----------
create table bank_Transaction(txt_no int not null,Account_no int not null,txt_type varchar(30) not null,txt_date DATETIME default current_timestamp);
alter table bank_transaction add constraint fk_key foreign key(Account_no) references bank_user(Account_no);
select*from bank_Transaction;
desc bank_transaction;
desc bank_user;
