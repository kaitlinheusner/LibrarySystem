import sqlite3
import datetime

def main():
    con = sqlite3.connect("library.db")
    cur = con.cursor()

    cur.execute("PRAGMA foreign_keys = ON")

    cur.execute("""CREATE TABLE IF NOT EXISTS libraryAccounts( 
                accountID INTEGER PRIMARY KEY AUTOINCREMENT,
                firstName TEXT,
                lastName TEXT,
                year INTEGER,
                UNIQUE(firstName, lastName))""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS libraryBooks(
                bookID INTEGER PRIMARY KEY AUTOINCREMENT,
                accountID INTEGER,
                title TEXT UNIQUE,
                Author TEXT,
                Year INTEGER,
                status TEXT,
                FOREIGN KEY(accountID) REFERENCES libraryAccounts(accountID))""")

    cur.execute("""
            INSERT OR IGNORE INTO libraryAccounts(firstName, lastName, year)
                       VALUES  
                       ('Samantha', 'Green', 2015),
                       ('Adam', 'Stone', 2020)""")

    cur.execute("""
            INSERT OR IGNORE INTO libraryBooks (accountID, title, Author, Year, status)
            VALUES
            (NULL, 'To Kill a Mockingbird', 'Harper Lee', 1960, 'Available'),
            (1, '1984', 'George Orwell', 1949, 'Checked Out'),
            (2, 'The Great Gatsby', 'F. Scott Fitzgerald', 1925, 'Available'),
            (NULL, 'Pride and Prejudice', 'Jane Austen', 1813, 'Available'),
            (NULL, 'The Hobbit', 'J.R.R. Tolkien', 1937, 'Checked Out'),
            (NULL, 'Fahrenheit 451', 'Ray Bradbury', 1953, 'Available'),
            (2, 'The Catcher in the Rye', 'J.D. Salinger', 1951, 'Available'),
            (NULL, 'Moby-Dick', 'Herman Melville', 1851, 'Checked Out'),
            (NULL, 'The Hunger Games', 'Suzanne Collins', 2008, 'Available'),
            ( NULL, 'Harry Potter and the Sorcerer''s Stone', 'J.K. Rowling', 1997, 'Checked Out')""")

    program_run = True

    while(program_run):
        print("Welcome to library catalog program!")
        print("What would you like to do?")
        print("1. Create Account")
        print("2. Borrow Book")
        print("3. Return Book")
        print("4. View All Account Records")
        print("5. View All Books")
        print("6. Show All Available Books")
        print("7. View All Authors")
        print("8. Find Account")
        print("9. Remove Book")
        print("10. Remove Account")
        print("11. Exit the program")

        try:
            userChoice = int(input("Enter your choice (use one of the numbers): "))
        except ValueError:
            print("Please enter a number")
            continue

        match userChoice:
            case 1:
                first_name = input("What is your first name? ")
                last_name = input("What is your last name? ")
                year = datetime.datetime.now().year

                sql_query = "INSERT INTO libraryAccounts(firstName, lastName, year) Values (?, ?, ?)" 

                cur.execute(sql_query, (first_name, last_name, year))

                con.commit()

                print(f"Account created successfully! Your account ID is {cur.lastrowid}")

                continue

            case 2:
                account_id = int(input("Enter your account ID: "))

                cur.execute("SELECT accountID FROM libraryAccounts WHERE accountID = ?", (account_id,))
                account_result = cur.fetchone()

                if not account_result:
                    print("We could not find an account associated with this ID." )
                    continue

                account_id = account_result[0]

                book_name = input ("What book would you like to borrow? ")
                cur.execute("SELECT bookID FROM libraryBooks WHERE title = ?", (book_name,))
                book_result = cur.fetchone()

                if book_result:
                    book_id = book_result[0]

                else:
                    print("We could not find this book!")
                    continue 

                sql_query = ("""
                        UPDATE libraryBooks
                        SET accountID = ?,  status = 'Checked Out'
                        WHERE bookID = ? AND status = 'Available'""")

                cur.execute(sql_query, (account_id, book_id))

                if cur.rowcount == 0:
                    print("This book is already checked out.")

                else: 
                    con.commit()
                    print("Book borrowed succesfully!")

                continue

            case 3:
                account_id = int(input("Enter your account ID: "))

                cur.execute("SELECT accountID FROM libraryAccounts WHERE accountID = ?", (account_id,))
                account_result = cur.fetchone()

                if not account_result:
                    print("We could not find an account associated with this ID.")
                    continue
                
                book_name = input("What book would you like to return? ")
                cur.execute("SELECT bookID FROM libraryBooks WHERE title = ? AND accountID = ? AND status = 'Checked Out'", (book_name, account_id))

                book_result = cur.fetchone()

                if not book_result:
                    print("This account does not have that book checked out.")
                    continue
                
                book_id = book_result[0]

                cur.execute("""
                    UPDATE libraryBooks
                    SET accountID = NULL, status = 'Available'
                    WHERE bookID = ?
                """, (book_id,))

                con.commit()

                print("Book returned successfully!")
                continue

            case 4:
                cur.execute("SELECT * FROM libraryAccounts")
                account_results =   cur.fetchall()

                for row in account_results:
                    print(row)

                continue

            case 5:
                cur.execute("SELECT * FROM libraryBooks")
                book_results = cur.fetchall()

                for row in book_results:
                    print(row)

                continue

            case 6:
                cur.execute("SELECT title FROM libraryBooks WHERE status = 'Available'")
                available_books = cur.fetchall()
                print("Available books:")
                for book in available_books:
                    print("-", book[0])

            case 7:
                cur.execute("SELECT DISTINCT author FROM libraryBooks")
                author_results = cur.fetchall()
                
                for author in author_results:
                    print(author)

                continue

            case 8:
                account_id = int(input("Enter your account ID: "))

                cur.execute("SELECT firstName, lastName, year FROM libraryAccounts WHERE accountID = ?", (account_id,))
                account_result = cur.fetchone()

                if account_result:
                    print(f"First Name: {account_result[0]}, Last Name: {account_result[1]}, Year Created: {account_result[2]}")

                else:
                    print("We could not find an account assosciated with this ID!")
                    continue 

                continue            

            case 9:
                book_name = input ("What book would you like to remove? ")  
                cur.execute("SELECT bookID FROM libraryBooks WHERE title = ?", (book_name,))
                book_result = cur.fetchone()

                if book_result:
                    cur.execute("DELETE FROM libraryBooks WHERE title = ?", (book_name,))
                    con.commit()

                    print("Book removed succesfully!")

                else:
                    print("We could not find this book!")
                    continue 

                continue

            case 10:
                account_id = int(input("Enter your account ID: "))
                cur.execute("SELECT accountID FROM libraryAccounts WHERE accountID = ?", (account_id,))
                account_result = cur.fetchone()

                if account_result:
                    cur.execute("SELECT * FROM libraryBooks WHERE accountID = ?", (account_result[0],))

                    if cur.fetchone():
                        print("Account has borrowed books. Cannot delete.")
                        continue

                    else:
                        con.execute("DELETE FROM libraryAccounts WHERE accountID = ?", (account_result[0],))
                        con.commit()
                        print("This account was deleted succesfully.")

                else:
                    print("We could not find an account associated with this ID!")
                    continue
                
                continue

            case 11:
                con.close()
                return
            
if __name__ == "__main__":
    main()
