import xml.etree.ElementTree as ET

def load_books_from_xml(filename):
    """Load books from an XML file and return a list of book dicts."""
    try:
        tree = ET.parse(filename)
    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'.")
        return []
    except ET.ParseError:
        print(f"Error: File '{filename}' is not valid XML.")
        return []

    root = tree.getroot()
    books = []

    for book_elem in root.findall("book"):
        title = book_elem.findtext("title", default="Unknown title")
        author = book_elem.findtext("author", default="Unknown author")
        year_text = book_elem.findtext("year", default="Unknown year")

        try:
            year = int(year_text)
        except ValueError:
            year = year_text

        books.append({
            "title": title,
            "author": author,
            "year": year
        })

    return books


def display_books(books):
    """Display all books."""
    print("Books in the XML file:\n")
    for book in books:
        print(f"- {book['title']} by {book['author']} ({book['year']})")


def find_book_by_title(books, title_to_find):
    """Return the book dict if the title matches (case-insensitive), else None."""
    title_to_find = title_to_find.lower()
    for book in books:
        if book["title"].lower() == title_to_find:
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
            print(f"Title:  {result['title']}")
            print(f"Author: {result['author']}")
            print(f"Year:   {result['year']}")
        else:
            print(f'\n"{user_input}" not found in the data.')


def main():
    filename = "session14/books.xml"

    # access and read the XML file and display its contents
    books = load_books_from_xml(filename)
    display_books(books)

    # repeatedly prompt for title, search, and display result
    search_loop(books)


if __name__ == "__main__":
    main()
