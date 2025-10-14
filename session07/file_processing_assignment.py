"""
File Processing Assignment
This program loads a list of names from 'names.txt', then repeatedly prompts
the user for a name to search. If the name is found, it displays a message.
If the name is not found, it writes the name to 'nofound.txt' and displays a message.
"""

def load_names():
    """
    Load all names from the 'names.txt' file into a list.
    Returns:
        list: A list of stripped names.
    """
    try:
        with open("session07/names.txt", "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Error: 'names.txt' not found.")
        return []


def search_name(name, name_list):
    """
    Check if a given name exists in the list.
    Parameters:
        name (str): The name to search for.
        name_list (list): The list of names to search in.
    Returns:
        bool: True if found, False otherwise.
    """
    if not name or not isinstance(name, str):
        return False
    return name.lower() in (n.lower() for n in name_list)


def write_not_found(name):
    """
    Append a name to 'nofound.txt' if not found.
    Parameters:
        name (str): The name to write.
    """
    try:
        with open("nofound.txt", "a") as file:
            file.write(name + "\n")
    except Exception as e:
        print(f"Error writing to 'nofound.txt': {e}")


def main():
    """
    Main function that controls program flow.
    """
    names = load_names()
    if not names:
        print("No names loaded. Exiting.")
        return

    while True:
        user_input = input("Enter a name (or 'quit' to exit): ").strip()
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        if search_name(user_input, names):
            print(f"{user_input} is in the list.")
        else:
            print(f"{user_input} not found. Adding to nofound.txt.")
            write_not_found(user_input)


if __name__ == "__main__":
    main()
