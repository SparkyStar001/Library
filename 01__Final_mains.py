import os, json, time, bcrypt, random
from datetime import datetime

# ------------------------------------------------------------
#   CLASS: UserInput
#   Purpose:
#   - Validates the user's name to ensure it only contains
#     letters and spaces.
# ------------------------------------------------------------
class UserInput:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        while True:
            # Check if name has only alphabets/spaces and is not empty
            if all(char.isalpha() or char.isspace() for char in self.name) and self.name.strip() != "":
                self.name = self.name
                print("Name accepted:", self.name)
                break
            else:
                print("Invalid input! Name should only contain letters and spaces.")

# ------------------------------------------------------------
#   CLASS: Storage_room
#   Purpose:
#   - Stores subscription details in JSON.
#   - Saves user data with timestamp and subscription code.
# ------------------------------------------------------------
class Storage_room:
    def __init__(self, name, Phone_Number, amount, sub_type, code, creationtime, t):
            self.name = name
            self.Phone_Number = Phone_Number
            self.amount = amount
            self.sub_type = sub_type
            self.code = code
            self.creationtime = creationtime
            self.t = t
    
    # Saves user subscription details
    def Daily_user(self):
        data = {
            "Name" : self.name,
            "Phone_Number" : self.Phone_Number,
            "Amount_Paid" : self.amount,
            "Unique code" : self.code,
            "type" : self.sub_type,
            "Time" : self.creationtime,
            "Time_time" : self.t
        }
        userfile = "02_Management.json"

        # Load existing data or create new list
        if os.path.exists(userfile):
            with open(userfile, "r") as J:
                try:
                    Reader_info = json.load(J)
                except json.JSONDecodeError:
                    Reader_info = []
        else: 
            Reader_info = []

        # Append new entry
        Reader_info.append(data)

        # Save file
        with open(userfile, 'w') as J:
            json.dump(Reader_info, J,indent=4)
        
# ------------------------------------------------------------
#   CLASS: Permission
#   Purpose:
#   - Asks user to confirm payment for subscription.
#   - If confirmed, proceeds to Payment class.
# ------------------------------------------------------------
class Permission:
    def __init__(self, amount):
        self.amount = amount

    # Ask confirmation for plan purchase
    def perm(self):
        perm = input(f"Amount Charged = {self.amount}, Are you sure ?(Y/N) :").lower()
        if perm == "y":
            amt = Payment(self.amount)
            amt.Payment_for_daily_users()
            time.sleep(2)
        elif perm == "n":
            print("Canceling request...")
            time.sleep(2)
            perm2 = input("Do you want to change the plan ? ").lower()
            if perm2 == "y":
                return
            elif perm2 == "n":
                print("Thanks for visiting us.")
                exit()
            else:
                print("Invalid input type")
                exit()
        else:
            print("Invalid input type")
            return

# ------------------------------------------------------------
#   FUNCTION: Printbook
#   Purpose:
#   - Displays book list from JSON.
#   - Optionally asks user if they want to borrow a book.
# ------------------------------------------------------------
def Printbook(name=None):
    booksfile = "03_Books.json"

    # Check file existence
    if os.path.exists(booksfile):
        try:
            with open(booksfile, "r") as f:
                booklist = json.load(f)
            print("Loading Book list...")
            time.sleep(1)
            print("Scanning file...")
            time.sleep(1)
            print("Scanning completed")
            time.sleep(1)
            print(json.dumps(booklist, indent=4))
        except json.JSONDecodeError:
            print("No Book Available")
            return
    else:
        print("File not found.")
        return

    # Ask user if they want to borrow a book
    if name is not None:
        ask = input("\nDo you want to borrow a book? (Y/N): ").lower()
        if ask == "y":
            BorrowBook(name)
        else:
            print("Okay, enjoy reading inside the library.")

# ------------------------------------------------------------
#   CLASS: Payment
#   Purpose:
#   - Handles payment checking through stored account records.
#   - Verifies PIN, checks balance, updates transaction history.
# ------------------------------------------------------------
class Payment:
    def __init__(self, amount):
        self.amount = amount

    # Payment handler for subscriptions & rent fees
    def Payment_for_daily_users(self):
        print("""==================
Make your payment
==================""")

        # Account number input validation
        try:
            Accountnumber  = int(input("Enter your Account number : "))
        except ValueError:
            print("Account number is a numerical Value.")
            print("Try again.")
            exit()

        # Pin input validation
        try:
            Entered_Pin  = int(input("Enter your Pin : "))
        except ValueError:
            print("Account number is a numerical Value.")
            print("Try again.")
            exit()

        print("Verifying...")
        time.sleep(1)
        print("Loading account details")
        time.sleep(2)
        print("Account loaded successfully.")
        time.sleep(2)

        print(f"Charged amount is {self.amount}")
        filename = "store.json"

        # Verify account existence and handle balance deduction
        if os.path.exists(filename):
            with open(filename, "r") as J:    
                try:
                    accounts = json.load(J)
                    found = False
                    for account in accounts:
                        if Accountnumber == int(account['account_number']):
                            found = True
                            stored_hashed_Pin = account['Pin']

                            # PIN Verification using bcrypt
                            if bcrypt.checkpw(str(Entered_Pin).encode(), stored_hashed_Pin.encode()):
                                current_balance = int(account["balance"])

                                # Check if funds are sufficient
                                if self.amount > current_balance:
                                    print(f"Insufficient Balance, your current balance is ₹{current_balance}.")
                                    return
                                else:
                                    # Deduct balance and update transaction
                                    account["balance"] = current_balance - self.amount
                                    print(f"Plan activated Successfully. Your New Balance is ₹{account['balance']}.")
                                    account["transactions"].append({
                                    "type": "Withdraw",
                                    "amount": self.amount,
                                    "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                                    })

                                    # Save updated data
                                    with open(filename, "w") as J:
                                        json.dump(accounts, J, indent=4)
                            else:
                                print("Incorrect Pin Entered ! ")
                            break

                    # If account number not found
                    if not found:
                        print("Your account is invalid.")
                        return

                except json.JSONDecodeError:
                    print("Sorry for inconvinence, This is us not you !")
                    exit()

# ------------------------------------------------------------
#   FUNCTION: oldvisiters
#   Purpose:
#   - Allows returning users to enter using unique subscription code.
#   - Validates subscription expiry based on plan duration.
# ------------------------------------------------------------
def oldvisiters():
    old_name = input("Enter you name : ")
    a = UserInput(old_name)
    a.get_name()

    try:
        uniquecode = input("Enter your unique code : ").strip()
    except ValueError:
        print("Code is a numerical value.")

    filename = "02_Management.json"

    if not os.path.exists(filename):
        print("File Error, This is us not you.")
        return

    found = False

    with open(filename, "r") as J:
        try:
            file = json.load(J)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format")
            return
        
    # Match user entry and calculate remaining subscription period
    for substore in file:
        stored_code = substore.get("Unique code")   
        subtype = substore.get("type")
        if stored_code is not None and uniquecode == stored_code:
            found = True
            createdtime = substore.get("Time_time")
            if createdtime is None:
                print("Error: Subscription time not recorded.")
                return

            a = time.time() - float(createdtime)

            # Subscription time validation
            if subtype == "Daily" and a > 86400:
                print("Your subscription period has been reached. Please buy a new sub to continue reading!")
            elif subtype == "Weekly" and a > 604800:
                print("Your subscription period has been reached. Please buy a new sub to continue reading!")
            elif subtype == "Monthly" and a > 2592000: 
                print("Your subscription period has been reached. Please buy a new sub to continue reading!")
            elif subtype == "Yearly" and a > 31536000: 
                print("Your subscription period has been reached. Please buy a new sub to continue reading!")
            else:
                print("Welcome to Library.")
                print("""
                1. View Books
                2. Borrow a Book
                3. Exit
                """)
                choice = input("Choose an option: ")

                if choice == "1":
                    Printbook(old_name)
                elif choice == "2":
                    BorrowBook(old_name)
                elif choice == "3":
                    print("Thanks for visiting!")
                else:
                    print("Invalid choice.")
            break 
    if not found:
        print("Account doesn't exist or code is invalid!")

# ------------------------------------------------------------
#   FUNCTION: code_gen
#   Purpose:
#   - Generates a unique 7-digit code ensuring no duplicates.
# ------------------------------------------------------------
def code_gen():
    filename = "02_Management.json"
    existing_codes = set()

    # Load already used codes to avoid duplicates
    if os.path.exists(filename):
        try:
            with open(filename, "r") as J:
                data = json.load(J)
                existing_codes = {str(entry.get("Unique code", "")) for entry in data}
        except (json.JSONDecodeError, FileNotFoundError):
            pass 
    
    # Generate new unused code
    while True:
        code = random.randint(10**6, 10**7 - 1)
        if str(code) not in existing_codes:
            return str(code)

# ------------------------------------------------------------
#   FUNCTION: BorrowBook
#   Purpose:
#   - Allows user to borrow a book for 1 - 7 days.
#   - Rent cost = 20% of book price per day.
#   - Ensures user cannot borrow more than one book at a time.
# ------------------------------------------------------------
def BorrowBook(name):
    booksfile = "03_Books.json"
    rentfile = "Rents.json"

    # Load books list
    if not os.path.exists(booksfile):
        print("No books available.")
        return

    with open(booksfile, "r") as f:
        try:
            books = json.load(f)
        except json.JSONDecodeError:
            print("Books data corrupted.")
            return

    # Load rent history
    if os.path.exists(rentfile):
        with open(rentfile, "r") as r:
            try:
                rent_data = json.load(r)
            except json.JSONDecodeError:
                rent_data = []
    else:
        rent_data = []

    # Prevent borrowing multiple books at the same time
    for entry in rent_data:
        if entry["Name"] == name and entry["Returned"] == False:
            print("You already have a borrowed book. Return it before borrowing a new one.")
            return
        
    # Display available books
    print("\nAvailable Books:\n")
    for i, book in enumerate(books, start=1):
        print(f"{i}. {book['title']} by {book['author']} - ₹{book['price']}")

    # Ask user to choose book
    try:
        choice = int(input("\nEnter the book number you want to borrow: "))
        if choice < 1 or choice > len(books):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid input.")
        return

    selected_book = books[choice - 1]
    price = float(selected_book["price"])

    # Ask rental days
    try:
        days = int(input("For how many days (1 to 7): "))
        if days < 1 or days > 7:
            print("Days must be between 1 and 7.")
            return
    except ValueError:
        print("Invalid input.")
        return

    # Cost = 20% of price × days
    cost = (price * 0.20) * days
    cost = int(cost)

    print(f"\nBorrow Cost = ₹{cost}")

    # Process payment
    pay = Payment(cost)
    pay.Payment_for_daily_users()

    borrow_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save borrow record
    rent_record = {
        "Name": name,
        "Book": selected_book["title"],
        "Days": days,
        "Cost": cost,
        "Borrow_Time": borrow_time,
        "Returned": False
    }

    rent_data.append(rent_record)

    with open(rentfile, "w") as w:
        json.dump(rent_data, w, indent=4)

    print(f"\nYou have borrowed '{selected_book['title']}' for {days} days.")

# ------------------------------------------------------------
#   FUNCTION: Main
#   Purpose:
#   - Entry point of program.
#   - Handles Admin and Reader workflow.
# ------------------------------------------------------------
def Main():
    print("""
=====================================
        Welcome to Library
=====================================
""")
    type = input("Admin / Reader (A/R): ").lower()

    # ------------------- Admin Section -------------------
    if type == "a":

        bookupdate = input("Do you want to update book details ?(Y/N) : ")
        if bookupdate == "y":
            count = int(input("How many books you want to add ? : "))
            new_books = []

            # Add new books
            for i in range (1, count + 1):
                book_title = input("Title: ")
                book_author = input("Author: ")
                book_price = input("Price: ")
                book = {
                    "title": book_title,
                    "author": book_author,
                    "price": book_price
                        }
                new_books.append(book)

            booksfile = "03_Books.json"

            # Load existing books or create new file
            if os.path.exists(booksfile):
                with open(booksfile, "r") as f:
                    try:
                        Availiblebook = json.load(f)
                    except json.JSONDecodeError:
                        Availiblebook = []
            else: 
                Availiblebook = []

            # Save books
            Availiblebook.extend(new_books)
            with open(booksfile, 'w') as f:
                json.dump(Availiblebook, f,indent=4)

        elif bookupdate == "n": 
            print("""1 : Clear managment file
2 : Clear Books file
                  """)
            try:
                admincall = int(input("Choose one option : "))
            except ValueError:
                print("Options are numerical !")
                return
            
            # Clear management records
            if admincall == 1:
                filename = "02_Management.json"
                with open(filename, "w") as file:
                    file.write("")
                    print("""Job done Sir
Thanks for coming hope so see you soon.""")

            # Clear books list
            elif admincall == 2:
                filename = "03_Books.json"
                with open(filename, 'w') as B:
                    json.dump([], B)
                    print("""Job done Sir
Thanks for coming hope so see you soon.""")
            else:
                print("Invalid input !")
        else: 
            print ("That's an invalid input.")

    # ------------------- Reader Section -------------------
    elif type =="r":
        oldornew = input("Do you have any subcription ?(Y/N) : ").lower()

        # Returning User
        if oldornew == "y":
            oldvisiters()

        # New User Subscription
        elif oldornew == "n":
            name = input("Enter Your name : ")
            name_verify = UserInput(name)
            name_verify.get_name()

            # Validate phone number
            try:
                Phone_Number = int(input("Enter your Contact number : "))
                Phone_Number = str(Phone_Number)
                if len(Phone_Number) < 10 or len(Phone_Number) > 10 : 
                    print("Invalid Number")
                    return 
            except ValueError:
                print("Phone number should be numerical only !")

            print("""
        D = Daily Subcribtion  for ₹ 50/-
        W = Weekly Subcribtion  for ₹ 300/-
        M = Monthly Subcribtion for ₹ 1,300/-
        Y = Yearly Subcribtion for ₹ 16,000/-
        """)

            # Subscription selection
            Subscibtion = input("Which Plan do you want to choose : ").lower()

            # Assign plan cost based on selection
            if Subscibtion == "d":
                amount = 50
                sub_type = "Daily"

            elif Subscibtion == "w":
                amount = 300
                sub_type = "Weekly"

            elif Subscibtion == "m":
                amount = 1300
                sub_type = "Monthly"

            elif Subscibtion == "y":
                amount = 16000
                sub_type = "Yearly"
            else:
                print("Choose a right input value, ")
                print("Thanks for visiting")
                exit() 

            # Confirm and process payment
            access = Permission(amount)
            access.perm()
            time.sleep(2)

            # Generate unique entry code
            code = code_gen()
            code = str(code)

            print(f"This is your unique code to enter next time within time limit {code}")

            # Ask whether to show books
            ask = input("Do you want to see availible books ?(Y/N) : ").lower()

            # Timestamp
            hour = time.localtime().tm_hour
            min = time.localtime().tm_min
            today = datetime.today()
            today = str(today)
            creationtime = (f"{hour}:{min} on {today[0:10]}")
            t = time.time()

            if ask == 'y':
                Printbook(name)
            elif ask == 'n':
                print("Thanks for visiting enjoy reading")
            else : 
                print("Enter a valid input")
                return

            # Store subscription history
            substore = Storage_room(name, Phone_Number, amount, sub_type, code, creationtime, t)
            substore.Daily_user()

        else:
            print("That's an invalid input : ")
    else:
        print("That's an invalid input : ")

# ------------------------------------------------------------
#   PROGRAM ENTRY POINT
# ------------------------------------------------------------
if __name__=='__main__':
    Main()
