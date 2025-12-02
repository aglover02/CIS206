import json

def load_books_from_json(filename):
    """Load books from a JSON file and return a list of book dicts."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'.")
        return []
    except json.JSONDecodeError:
        print(f"Error: File '{filename}' is not valid JSON.")
        return []

    # Expecting a top-level "books" list
    books = data.get("books", [])
    return books


def display_books(books):
    """Display all books."""
    print("Books in the file:\n")
    for book in books:
        title = book.get("title", "Unknown title")
        author = book.get("author", "Unknown author")
        year = book.get("year", "Unknown year")
        print(f"- {title} by {author} ({year})")


def find_book_by_title(books, title_to_find):
    """Return the book dict if the title matches (case-insensitive), else None."""
    title_to_find = title_to_find.lower()
    for book in books:
        title = book.get("title", "")
        if title.lower() == title_to_find:
            return book
    return None


def search_loop(books):
    """Repeatedly prompt the user for a book title and display the result."""
    if not books:
        print("No books available to search.")
        return

    while True:
        user_input = input("\nEnter a book title (or press Enter to quit): ").strip()
        if user_input == "":
            print("Exiting search. Goodbye!")
            break

        result = find_book_by_title(books, user_input)

        if result is not None:
            print("\nBook found:")
            print(f"Title:  {result.get('title', 'Unknown')}")
            print(f"Author: {result.get('author', 'Unknown')}")
            print(f"Year:   {result.get('year', 'Unknown')}")
        else:
            print(f'\n"{user_input}" not found in the data.')


def main():
    filename = "session14/books.json"

    # access and read the JSON file and display its contents
    books = load_books_from_json(filename)
    display_books(books)

    # repeatedly prompt for title, search, and display result
    search_loop(books)


if __name__ == "__main__":
    main()