"""
BMI Calculator (Imperial to Metric) with Validation, Error Handling, and Looping.

This program prompts the user to enter their weight in pounds,
and their height in feet and inches. It then calculates the
Body Mass Index (BMI) using the imperial formula:

    BMI = (weight_lbs / (total_height_in)**2) * 703

Enhancements:
- Validation and exception handling.
- Re-prompts user instead of terminating on invalid input.
- User can type "q" to quit the program at any time.
- Main program loops to allow multiple BMI calculations until user quits.
"""

# Constants for BMI category thresholds (kg/m^2)
UNDERWEIGHT_THRESHOLD = 18.5
OVERWEIGHT_THRESHOLD = 25.0


def get_user_input():
    """
    Prompt the user for weight and height values.

    Returns:
        tuple[float, int, int] | None:
            A tuple containing weight in pounds, height in feet,
            and height in inches, or None if the user chooses to quit.

    Raises:
        ValueError: If weight or height values are invalid.
        Exception: For any unexpected error during input.

    Notes:
        - Accepts "q" at any prompt to quit.
        - Performs nested if validation for zero feet and small inches.
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

            # Nested if validation
            if height_feet == 0:
                if height_inches < 36:  # arbitrary lower bound
                    raise ValueError("Height in inches is too short to be valid.")

            return weight_lbs, height_feet, height_inches

        except ValueError as ve:
            print(f"Input error: {ve}. Please try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")


def calculate_bmi(weight_lbs, height_feet, height_inches):
    """
    Calculate BMI using imperial units with parameter validation.

    Args:
        weight_lbs (float): Weight in pounds.
        height_feet (int): Height in feet component.
        height_inches (int): Height in inches component.

    Returns:
        float: The calculated BMI value.

    Raises:
        ValueError: If total height is zero or negative.
        AssertionError: If BMI falls outside a realistic human range.
    """
    total_height_inches = height_feet * 12 + height_inches
    
    if total_height_inches <= 0:
        raise ValueError("Total height must be greater than zero.")

    bmi = (weight_lbs / (total_height_inches ** 2)) * 703

    assert 5 <= bmi <= 100, "Calculated BMI is outside realistic human range."

    return bmi


def display_bmi_and_legend(bmi_value):
    """
    Display the BMI result and category legend.

    Args:
        bmi_value (float): The calculated BMI value.

    Returns:
        None
    """
    print(f"\nYour BMI is: {bmi_value:.1f}\n")
    print("BMI Category Legend (kg/m²):")
    print(f"  Underweight: less than {UNDERWEIGHT_THRESHOLD}")
    print(f"  Normal weight: {UNDERWEIGHT_THRESHOLD} to less than {OVERWEIGHT_THRESHOLD}")
    print(f"  Overweight: {OVERWEIGHT_THRESHOLD} or greater")
    print("-" * 40)


def main():
    """
    Run the BMI calculator program.

    The program loops continuously, prompting the user for weight and height,
    calculating BMI, and displaying results until the user chooses to quit.

    Returns:
        None
    """
    while True:
        try:
            user_data = get_user_input()
            if user_data is None:
                print("Program terminated by user.")
                break
            weight_lbs, height_feet, height_inches = user_data
            bmi_result = calculate_bmi(weight_lbs, height_feet, height_inches)
            display_bmi_and_legend(bmi_result)
        except AssertionError as ae:
            print(f"Assertion failed: {ae}")
        except Exception as e:
            print(f"An error occurred in the program: {e}")


if __name__ == "__main__":
    main()