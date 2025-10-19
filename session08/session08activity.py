"""
Reads customer records from `northwindCustomers.txt` and provides a menu to
display or search customers using lists/tuples and standalone functions.
"""

from __future__ import annotations

import csv
from typing import Iterable, List, Sequence, Tuple

# Each customer is a (company, contact, phone) tuple.
Customer = Tuple[str, str, str]

def load_customers(path: str) -> List[Customer]:
    """
    Load customers from a CSV text file.

    Parameters
    path : str
        Path to the input file (e.g., 'northwindCustomers.txt').

    Returns
    List[Customer]
        A list of (company, contact, phone) tuples. Records with missing
        required fields are skipped with basic validation.
    """
    if not isinstance(path, str) or not path.strip():
        raise ValueError("path must be a non-empty string")

    customers: List[Customer] = []
    skipped = 0

    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            for row in reader:
                # Basic validation and normalization
                if row is None:
                    skipped += 1
                    continue
                parts = [p.strip() for p in row]
                if len(parts) < 3:
                    skipped += 1
                    continue
                company, contact, phone = parts[0], parts[1], parts[2]
                if not company or not contact or not phone:
                    skipped += 1
                    continue
                customers.append((company, contact, phone))
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        return []
    except OSError as e:
        print(f"Error reading '{path}': {e}")
        return []

    if skipped:
        print(f"Note: skipped {skipped} invalid record(s).")
    return customers

def sort_customers(customers: Sequence[Customer], key_index: int) -> List[Customer]:
    """
    Return a new list of customers sorted by the specified field index.

    Parameters
    customers : Sequence[Customer]
        The list/sequence of customers to sort.
    key_index : int
        0 for company name, 1 for contact name.

    Returns
    List[Customer]
        Sorted list of customers.

    Raises
    ValueError
        If key_index is not 0 or 1.
    """
    if key_index not in (0, 1):
        raise ValueError("key_index must be 0 (company) or 1 (contact)")
    # Defensive copy and sort case-insensitively
    return sorted(list(customers), key=lambda c: (c[key_index] or "").lower())

def display_records(records: Iterable[Customer], *, order_label: str) -> None:
    """
    Display customer records with aligned columns.

    Parameters
    records : Iterable[Customer]
        Customers to display.
    order_label : str
        Label indicating the sort order (for the header only).
    """
    header = f"Customers ({order_label})"
    print("\n" + header)
    print("-" * len(header))

    # Convert to list for width calculation
    rows = list(records)
    if not rows:
        print("No records to display.\n")
        return

    # Compute column widths
    company_w = max(len("Company Name"), *(len(c[0]) for c in rows))
    contact_w = max(len("Contact Name"), *(len(c[1]) for c in rows))
    phone_w = max(len("Phone Number"), *(len(c[2]) for c in rows))

    # Print header
    print(f"{'Company Name'.ljust(company_w)}  "
          f"{'Contact Name'.ljust(contact_w)}  "
          f"{'Phone Number'.ljust(phone_w)}")
    print(f"{'-'*company_w}  {'-'*contact_w}  {'-'*phone_w}")

    # Print rows
    for company, contact, phone in rows:
        print(f"{company.ljust(company_w)}  "
              f"{contact.ljust(contact_w)}  "
              f"{phone.ljust(phone_w)}")
    print()  # trailing newline

def search_customers(customers: Sequence[Customer], query: str, field_index: int) -> List[Customer]:
    """
    Search customers for a case-insensitive substring match on a field.

    Parameters
    customers : Sequence[Customer]
        Customers to search.
    query : str
        Search string (non-empty). Substring matches are returned.
    field_index : int
        0 for company name, 1 for contact name.

    Returns
    List[Customer]
        Matching customers (in original order).

    Raises
    ValueError
        If query is empty or field_index invalid.
    """
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must be a non-empty string")
    if field_index not in (0, 1):
        raise ValueError("field_index must be 0 (company) or 1 (contact)")

    q = query.lower()
    return [c for c in customers if q in (c[field_index] or "").lower()]

def display_labeled(records: Iterable[Customer]) -> None:
    """
    Display customers with field labels on each line.

    Parameters
    records : Iterable[Customer]
        Records to display.
    """
    rows = list(records)
    if not rows:
        print("No matching records.\n")
        return
    print()
    for company, contact, phone in rows:
        print(f"Company Name : {company}")
        print(f"Contact Name : {contact}")
        print(f"Phone Number : {phone}")
        print("-" * 40)
    print()

def print_menu() -> None:
    """Print the main menu options."""
    print("1. Display customers sorted by company name")
    print("2. Display customers sorted by contact name")
    print("3. Search customers by company name")
    print("4. Search customers by contact name")
    print("5. Exit")

def get_menu_choice() -> int:
    """
    Prompt the user for a menu choice (1-5).

    Returns
    int
        The selected option as an integer.
    """
    while True:
        choice = input("Select an option (1-5): ").strip()
        if not choice:
            print("Please enter a choice.")
            continue
        if not choice.isdigit():
            print("Please enter a number from 1 to 5.")
            continue
        num = int(choice)
        if 1 <= num <= 5:
            return num
        print("Choice out of range. Try again.")

def prompt_non_empty(prompt: str) -> str:
    """
    Prompt for a non-empty string input.

    Parameters
    prompt : str
        The prompt to show.

    Returns
    str
        The trimmed, non-empty user input.
    """
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Input cannot be empty. Try again.")

def run_cli(path: str = "session08/northwindCustomers.txt") -> None:
    """
    Run the menu-driven CLI for the Northwind customers file.

    Parameters
    path : str, optional
        File path to load, by default 'northwindCustomers.txt'.
    """
    customers = load_customers(path)
    if not customers:
        print("No data loaded. Exiting.")
        return

    while True:
        print_menu()
        choice = get_menu_choice()

        if choice == 1:
            sorted_rows = sort_customers(customers, key_index=0)
            display_records(sorted_rows, order_label="sorted by Company Name")
        elif choice == 2:
            sorted_rows = sort_customers(customers, key_index=1)
            display_records(sorted_rows, order_label="sorted by Contact Name")
        elif choice == 3:
            q = prompt_non_empty("Enter company name (or part of it): ")
            matches = search_customers(customers, q, field_index=0)
            display_labeled(matches)
        elif choice == 4:
            q = prompt_non_empty("Enter contact name (or part of it): ")
            matches = search_customers(customers, q, field_index=1)
            display_labeled(matches)
        elif choice == 5:
            print("Goodbye!")
            break


if __name__ == "__main__":
    run_cli()