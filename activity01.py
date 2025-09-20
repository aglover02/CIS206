"""
BMI Calculator (Imperial to Metric) with Validation and Error Handling

This program prompts the user to enter their weight in pounds,
and their height in feet and inches. It then calculates the
Body Mass Index (BMI) using the imperial formula:

    BMI = (weight_lbs / (total_height_in)**2) * 703

Validation and exception handling have been added:
- Data type validation and range validation.
- Assertions to confirm calculated values are reasonable.
- Exception handling with try/except blocks.
- Nested if statements used within validation.
- Re-prompts user instead of terminating on invalid input.
- User can type "q" to quit the program at any time.
"""

# Constants for BMI category thresholds (kg/m^2)
UNDERWEIGHT_THRESHOLD = 18.5
OVERWEIGHT_THRESHOLD = 25.0


def get_user_input():
    """
    Prompt user to enter weight in pounds, then height in feet and inches.
    Returns a tuple: (weight_lbs, height_feet, height_inches).
    Includes exception handling and validation (#1, #2, #3).
    User can quit by typing 'q'.
    """
    while True:
        try:
            weight_input = input("Enter your weight in pounds (or 'q' to quit): ")
            if weight_input.lower() == "q":
                return None
            weight_lbs = float(weight_input)

            feet_input = input("Enter your height - feet component (or 'q' to quit): ")
            if feet_input.lower() == "q":
                return None
            height_feet = int(feet_input)

            inches_input = input("Enter your height - inches component (or 'q' to quit): ")
            if inches_input.lower() == "q":
                return None
            height_inches = int(inches_input)

            # Validation checks
            if weight_lbs <= 0:
                raise ValueError("Weight must be a positive number.")
            if height_feet < 0 or height_inches < 0:
                raise ValueError("Height components must not be negative.")

            # Nested if example 
            if height_feet == 0:
                if height_inches < 36:  # arbitrary lower bound
                    raise ValueError("Height in inches is too short to be valid.")

            return weight_lbs, height_feet, height_inches

        except ValueError as ve:
            print(f"Input error: {ve}. Please try again.")
        except Exception as e:  # catch-all
            print(f"Unexpected error: {e}. Please try again.")


def calculate_bmi(weight_lbs, height_feet, height_inches):
    """
    Calculate BMI using imperial units with parameter validation (#1).
    
    Converts height in feet and inches to total inches, then applies:
        BMI = (weight_lbs / (height_in_inches ** 2)) * 703
    
    Returns BMI as a float.
    """
    total_height_inches = height_feet * 12 + height_inches
    
    # Range validation 
    if total_height_inches <= 0:
        raise ValueError("Total height must be greater than zero.")

    bmi = (weight_lbs / (total_height_inches ** 2)) * 703

    # Assertion to ensure BMI is realistic 
    assert 5 <= bmi <= 100, "Calculated BMI is outside realistic human range."

    return bmi


def display_bmi_and_legend(bmi_value):
    """
    Display the BMI value formatted to one decimal place,
    and print the legend for BMI categories.
    """
    print(f"\nYour BMI is: {bmi_value:.1f}\n")
    print("BMI Category Legend (kg/m²):")
    print(f"  Underweight: less than {UNDERWEIGHT_THRESHOLD}")
    print(f"  Normal weight: {UNDERWEIGHT_THRESHOLD} to less than {OVERWEIGHT_THRESHOLD}")
    print(f"  Overweight: {OVERWEIGHT_THRESHOLD} or greater")


def main():
    """
    Main function to run the BMI calculator program with exception handling (#2).
    """
    try:
        user_data = get_user_input()
        if user_data is None:  # user chose to quit
            print("Program terminated by user.")
            return
        weight_lbs, height_feet, height_inches = user_data
        bmi_result = calculate_bmi(weight_lbs, height_feet, height_inches)
        display_bmi_and_legend(bmi_result)
    except AssertionError as ae:  # specific exception handling 
        print(f"Assertion failed: {ae}")
    except Exception as e:  # catch-all safety net 
        print(f"An error occurred in the program: {e}")


if __name__ == "__main__":
    main()
