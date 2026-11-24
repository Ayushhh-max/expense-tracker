import sqlite3

class LibrarySystem:
    def __init__(self, db_name="library.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                total_copies INTEGER NOT NULL,
                available_copies INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def add_book(self, title, author, copies):
        self.cursor.execute(
            "INSERT INTO books (title, author, total_copies, available_copies) VALUES (?, ?, ?, ?)",
            (title, author, copies, copies)
        )
        self.conn.commit()
        print(f"\n[Success] Added '{title}' by {author} ({copies} copies).")

    def view_books(self):
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        print("\n--- Library Catalog ---")
        if not books:
            print("No books in the library yet.")
        else:
            print(f"{'ID':<5} {'Title':<25} {'Author':<20} {'Available/Total'}")
            print("-" * 65)
            for book in books:
                print(f"{book[0]:<5} {book[1]:<25} {book[2]:<20} {book[4]}/{book[3]}")

    def search_book(self, keyword):
        self.cursor.execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
            (f"%{keyword}%", f"%{keyword}%")
        )
        results = self.cursor.fetchall()
        print(f"\n--- Search Results for '{keyword}' ---")
        if not results:
            print("No matching books found.")
        else:
            for book in results:
                print(f"ID: {book[0]} | '{book[1]}' by {book[2]} (Available: {book[4]}/{book[3]})")

    def borrow_book(self, book_id):
        self.cursor.execute("SELECT title, available_copies FROM books WHERE id = ?", (book_id,))
        book = self.cursor.fetchone()
        
        if not book:
            print("\n[Error] Book ID not found.")
        elif book[1] <= 0:
            print(f"\n[Unavailable] All copies of '{book[0]}' are currently checked out.")
        else:
            self.cursor.execute(
                "UPDATE books SET available_copies = available_copies - 1 WHERE id = ?",
                (book_id,)
            )
            self.conn.commit()
            print(f"\n[Success] You borrowed '{book[0]}'.")

    def return_book(self, book_id):
        self.cursor.execute("SELECT title, available_copies, total_copies FROM books WHERE id = ?", (book_id,))
        book = self.cursor.fetchone()
        
        if not book:
            print("\n[Error] Book ID not found.")
        elif book[1] >= book[2]:
            print(f"\n[Error] All copies of '{book[0]}' are already in the library.")
        else:
            self.cursor.execute(
                "UPDATE books SET available_copies = available_copies + 1 WHERE id = ?",
                (book_id,)
            )
            self.conn.commit()
            print(f"\n[Success] Returned '{book[0]}'.")

    def close(self):
        self.conn.close()


def main():
    library = LibrarySystem()
    
    while True:
        print("\n=== Library Management System ===")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Book")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            title = input("Enter book title: ").strip()
            author = input("Enter author name: ").strip()
            try:
                copies = int(input("Enter number of copies: "))
                if copies > 0:
                    library.add_book(title, author, copies)
                else:
                    print("\n[Error] Copies must be greater than 0.")
            except ValueError:
                print("\n[Error] Please enter a valid number.")
                
        elif choice == '2':
            library.view_books()
            
        elif choice == '3':
            keyword = input("Enter title or author to search: ").strip()
            library.search_book(keyword)
            
        elif choice == '4':
            try:
                book_id = int(input("Enter Book ID to borrow: "))
                library.borrow_book(book_id)
            except ValueError:
                print("\n[Error] Please enter a valid numeric ID.")
                
        elif choice == '5':
            try:
                book_id = int(input("Enter Book ID to return: "))
                library.return_book(book_id)
            except ValueError:
                print("\n[Error] Please enter a valid numeric ID.")
                
        elif choice == '6':
            library.close()
            print("Goodbye!")
            break
            
        else:
            print("\n[Error] Invalid option. Please choose 1-6.")

if __name__ == "__main__":
    main()