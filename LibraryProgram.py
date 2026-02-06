import sqlite3
import datetime

def main():
    conAccount = sqlite3.connect("libraryAccounts.db")
    conBooks = sqlite3.connect("libraryBooks.db")
    curAccount = conAccount.cursor()
    curBooks = conBooks.cursor()

    curAccount.execute("""CREATE TABLE IF NOT EXISTS libraryAccounts( 
                accountID INTEGER PRIMARY KEY AUTOINCREMENT,
                firstName TEXT,
                lastName TEXT,
                year INTEGER)""")
    
    curBooks.execute("""CREATE TABLE IF NOT EXISTS libraryBooks(
                bookId INTEGER PRIMARY KEY AUTOINCREMENT,
                accountID INTEGER,
                title TEXT,
                Author TEXT,
                Year INTEGER,
                status TEXT,
                FOREIGN KEY(accountID) REFERENCES libraryAccounts(accountID))""")


    curAccount.execute("""
            INSERT INTO libraryAccounts(firstName, lastName, year)
                       VALUES  
                       ('Samantha', 'Green', 2015),
                       ('Adam', 'Stone', 2020)""")

    curBooks.execute("""
            INSERT OR IGNORE INTO libraryBooks (bookId, accountID, title, Author, Year, status)
            VALUES
            (1, NULL, 'To Kill a Mockingbird', 'Harper Lee', 1960, 'Available'),
            (2, 1, '1984', 'George Orwell', 1949, 'Checked Out'),
            (3, 2, 'The Great Gatsby', 'F. Scott Fitzgerald', 1925, 'Available'),
            (4, NULL, 'Pride and Prejudice', 'Jane Austen', 1813, 'Available'),
            (5, NULL, 'The Hobbit', 'J.R.R. Tolkien', 1937, 'Checked Out'),
            (6, NULL, 'Fahrenheit 451', 'Ray Bradbury', 1953, 'Available'),
            (7, 2, 'The Catcher in the Rye', 'J.D. Salinger', 1951, 'Available'),
            (8, NULL, 'Moby-Dick', 'Herman Melville', 1851, 'Checked Out'),
            (9, NULL, 'The Hunger Games', 'Suzanne Collins', 2008, 'Available'),
            (10, NULL, 'Harry Potter and the Sorcerer''s Stone', 'J.K. Rowling', 1997, 'Checked Out')""")


    print("Welcome to library catalog program!")
    print("What would you like to do?")
    print("1. Create Account")
    print("2. Borrow Book")
    print("3. Return Book")
    print("4. View All Account Records")
    print("5. View All Books")
    print("6. View All Authors")
    print("7. Find Account")
    print("8. Remove Book")
    print("9. Remove Account")

    try:
        userChoice = int(input("Enter your choice (use one of the numbers): "))
    except ValueError:
        print("Please enter a number")

    match userChoice:
        case 1:
            first_name = input("What is your first name?")
            last_name = input("What is your last name?")
            year = datetime.datetime.now().year

            sql_query = "INSERT INTO libraryAccounts(firstName, lastName, year) Values (?, ?, ?)" 

            curAccount.execute(sql_query, (first_name, last_name, year))

            conAccount.commit()

            print("Account created succesfully")
            return
        
        case 2:
            first_name = input("What is your first name?")
            last_name = input("What is your last name?")

            curAccount.execute("SELECT accountID FROM libraryAccounts WHERE firstName = ? AND lastName = ?", (first_name, last_name))
            account_result = curAccount.fetchone()

            if account_result:
                account_id = account_result[0]

            else:
                print("We could not find an account assosciated with this name!")
                return 

            book_name = input ("What book would you like to borrow?")
            curBooks.execute("SELECT bookID FROM libraryBooks WHERE title = ?", (book_name))
            book_result = curBooks.fetchone()

            if book_result:
                book_id = book_result[0]

            else:
                print("We could not find this book!")
                return 

            sql_query = ("""
                    UPDATE libraryBooks
                    SET accountID = ?,  status = 'Checked Out'
                    WHERE bookId = ? AND accountID IS NULL""")
            
            curBooks.execute(sql_query, (book_id, account_id))
            conBooks.commit()

            print("Book borrowed succesfully!")

        case 3:
            book_name = input ("What book would you like to return?")  
            curBooks.execute("SELECT bookID FROM libraryBooks WHERE title ", (book_name,))
            book_result = curBooks.fetchone()

            if book_result:
                book_id = book_result[0]

            else:
                print("We could not find this book!")
                return 
            
            sql_query = ("""
                    UPDATE libraryBooks
                    SET accountID = NULL,  status = 'Available'
                    WHERE bookId = ?""")
            
            curBooks.execute(sql_query, (book_id,))
            conBooks.commit()
            print("Book returned succesfully")
            return

        case 4:
            curAccount.execute("SELECT * FROM libraryAccounts")
            account_results = curAccount.fetchall()
            
            for row in account_results:
                print(row)
            
            return
        
        case 5:
            curBooks.execute("SELECT * FROM libraryBooks")
            book_results = curBooks.fetchall()

            for row in book_results:
                print(row)

            return

        case 6:
            curBooks.execute("SELECT author FROM libraryBooks")
            author_results = curAccount.fetchone()
            print(author_results)
            return

        case 7:
            first_name = input("What is your first name?")
            last_name = input("What is your last name?")

            account_id = curAccount.execute("SELECT accountID FROM libraryAccounts WHERE firstName = ? AND lastName = ?", (first_name, last_name))
            account_result = curAccount.fetchone()

            if account_result:
                account_id = account_result

            else:
                print("We could not find an account assosciated with this name!")
                return 
            return            
        
        case 8:
            book_name = input ("What book would you like to remove?")  
            book_id = curBooks.execute("SELECT bookID FROM libraryBooks WHERE title ", (book_name,))
            book_result = curBooks.fetchone()

            if book_result:
                conBooks.execute("DELETE FROM libraryBooks WHERE title ?", (book_name,))
                conBooks.commit()

                print("Book removed succesfully!")

            else:
                print("We could not find this book!")
                return 
            
            return
            
        case 9:
            first_name = input("What is your first name?")
            last_name = input("What is your last name?")

            curAccount.execute("SELECT accountID FROM libraryAccounts WHERE firstName ? AND lastName ?", (first_name, last_name))
            account_result = curAccount.fetchone()

            if account_result:
                conAccount.execute("DELETE FROM libraryAccounts WHERE firstName ? AND lastName ?", (first_name, last_name))
                conAccount.commit()

                print("This account was deleted succesfully.")

            else:
                print("We could not find an account associated with this name!")
                return
            
            return

if __name__ == "__main__":
    main()
