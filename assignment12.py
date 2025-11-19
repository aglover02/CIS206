from datetime import date


# Employee Class
class Employee:
    def __init__(self, name="", idNumber=0, department="", position=""):
        """
        This single constructor can act as:
        - Default constructor: Employee()
        - Name + ID constructor: Employee("Name", 12345)
        - Full constructor: Employee("Name", 12345, "Dept", "Position")
        """
        self.__name = name
        self.__idNumber = idNumber
        self.__department = department
        self.__position = position

    # Mutators (setters)
    def set_name(self, name):
        self.__name = name

    def set_idNumber(self, idNumber):
        self.__idNumber = idNumber

    def set_department(self, department):
        self.__department = department

    def set_position(self, position):
        self.__position = position

    # Accessors (getters)
    def get_name(self):
        return self.__name

    def get_idNumber(self):
        return self.__idNumber

    def get_department(self):
        return self.__department

    def get_position(self):
        return self.__position


# Patient Class

class Patient:
    def __init__(self, first_name, middle_name, last_name,
                 address, city, state, zip_code,
                 phone_number,
                 emergency_contact_name, emergency_contact_phone):
        self.__first_name = first_name
        self.__middle_name = middle_name
        self.__last_name = last_name
        self.__address = address
        self.__city = city
        self.__state = state
        self.__zip_code = zip_code
        self.__phone_number = phone_number
        self.__emergency_contact_name = emergency_contact_name
        self.__emergency_contact_phone = emergency_contact_phone

    # Mutators (setters)
    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_middle_name(self, middle_name):
        self.__middle_name = middle_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_address(self, address):
        self.__address = address

    def set_city(self, city):
        self.__city = city

    def set_state(self, state):
        self.__state = state

    def set_zip_code(self, zip_code):
        self.__zip_code = zip_code

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_emergency_contact_name(self, name):
        self.__emergency_contact_name = name

    def set_emergency_contact_phone(self, phone):
        self.__emergency_contact_phone = phone

    # Accessors (getters)
    def get_first_name(self):
        return self.__first_name

    def get_middle_name(self):
        return self.__middle_name

    def get_last_name(self):
        return self.__last_name

    def get_address(self):
        return self.__address

    def get_city(self):
        return self.__city

    def get_state(self):
        return self.__state

    def get_zip_code(self):
        return self.__zip_code

    def get_phone_number(self):
        return self.__phone_number

    def get_emergency_contact_name(self):
        return self.__emergency_contact_name

    def get_emergency_contact_phone(self):
        return self.__emergency_contact_phone

# Procedure Class

class Procedure:
    def __init__(self, name, date, practitioner, charge):
        self.__name = name
        self.__date = date
        self.__practitioner = practitioner
        self.__charge = charge

    # Mutators (setters)
    def set_name(self, name):
        self.__name = name

    def set_date(self, date):
        self.__date = date

    def set_practitioner(self, practitioner):
        self.__practitioner = practitioner

    def set_charge(self, charge):
        self.__charge = charge

    # Accessors (getters)
    def get_name(self):
        return self.__name

    def get_date(self):
        return self.__date

    def get_practitioner(self):
        return self.__practitioner

    def get_charge(self):
        return self.__charge


# Test Program

def test_employees():
    print("=== Employee Test Cases ===")

    # Using full constructor
    emp1 = Employee("Susan Meyers", 47899, "Accounting", "Vice President")
    # Using name + ID (department and position default to "")
    emp2 = Employee("Mark Jones", 39119)
    emp2.set_department("IT")
    emp2.set_position("Programmer")
    # Using default constructor then setters
    emp3 = Employee()
    emp3.set_name("Joy Rogers")
    emp3.set_idNumber(81774)
    emp3.set_department("Manufacturing")
    emp3.set_position("Engineer")

    employees = [emp1, emp2, emp3]

    for i, e in enumerate(employees, start=1):
        print(f"\nEmployee #{i}")
        print(f"Name:       {e.get_name()}")
        print(f"ID Number:  {e.get_idNumber()}")
        print(f"Department: {e.get_department()}")
        print(f"Position:   {e.get_position()}")


def test_patient_and_procedures():
    print("\n=== Patient and Procedure Test Cases ===")

    # Create a patient with sample data
    patient = Patient(
        first_name="John",
        middle_name="A.",
        last_name="Doe",
        address="123 Main St",
        city="Springfield",
        state="IL",
        zip_code="62701",
        phone_number="555-123-4567",
        emergency_contact_name="Jane Doe",
        emergency_contact_phone="555-987-6543"
    )

    # Today's date as a string
    todays_date = date.today().strftime("%m/%d/%Y")

    # Create three procedures
    proc1 = Procedure("Physical Exam", todays_date, "Dr. Irvine", 250.00)
    proc2 = Procedure("X-ray",         todays_date, "Dr. Jaminson",    500.00)
    proc3 = Procedure("Blood test",    todays_date, "Dr. Smith",  200.00)

    procedures = [proc1, proc2, proc3]

    # Display patient information
    print("\nPatient Information:")
    full_name = f"{patient.get_first_name()} {patient.get_middle_name()} {patient.get_last_name()}"
    print(f"Name:          {full_name}")
    print(f"Address:       {patient.get_address()}")
    print(f"City/State/ZIP:{patient.get_city()}, {patient.get_state()} {patient.get_zip_code()}")
    print(f"Phone:         {patient.get_phone_number()}")
    print(f"Emergency Contact: {patient.get_emergency_contact_name()}")
    print(f"Emergency Phone:   {patient.get_emergency_contact_phone()}")

    # Display procedures and total charges
    print("\nProcedures:")
    total_charges = 0.0
    for i, p in enumerate(procedures, start=1):
        print(f"\nProcedure #{i}")
        print(f"Name:         {p.get_name()}")
        print(f"Date:         {p.get_date()}")
        print(f"Practitioner: {p.get_practitioner()}")
        print(f"Charge:       ${p.get_charge():.2f}")
        total_charges += p.get_charge()

    print(f"\nTotal Charges for all procedures: ${total_charges:.2f}")


def main():
    test_employees()
    test_patient_and_procedures()


if __name__ == "__main__":
    main()