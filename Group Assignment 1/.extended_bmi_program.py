"""
BMI Calculator with Separate Functions 

This program calculates a user's Body Mass Index (BMI) based on
their weight in pounds and height in feet and inches. It uses
separate functions for input collection, unit conversions, BMI
calculation, and output display.

BMI Formula (metric units):
    BMI = weight_kg / (height_m ** 2)

Conversion factors:
    - 1 foot = 12 inches
    - 1 pound = 0.45359237 kilograms
    - 1 inch = 0.0254 meters

BMI Categories (WHO standard):
    Underweight: BMI < 18.5
    Normal weight: 18.5 ≤ BMI < 25.0
    Overweight: BMI ≥ 25.0
"""

# Constants for conversions
FEET_TO_INCHES = 12
POUNDS_TO_KILOGRAMS = 0.45359237
INCHES_TO_METERS = 0.0254

# BMI thresholds
UNDERWEIGHT_THRESHOLD = 18.5
OVERWEIGHT_THRESHOLD = 25.0


# Input Functions
def get_weight_pounds():
    """
    Prompt the user to enter their weight in pounds.

    Returns:
        float: Weight in pounds.
    """
    return float(input("Enter your weight in pounds: "))


def get_height_feet():
    """
    Prompt the user to enter the feet portion of their height.

    Returns:
        int: Height in feet.
    """
    return int(input("Enter your height (feet): "))


def get_height_inches():
    """
    Prompt the user to enter the inches portion of their height.

    Returns:
        int: Height in inches.
    """
    return int(input("Enter your height (inches): "))


# Conversion Functions
def convert_weight_to_kilograms(weight_pounds):
    """
    Convert weight from pounds to kilograms.

    Args:
        weight_pounds (float): Weight in pounds.

    Returns:
        float: Weight in kilograms.
    """
    return weight_pounds * POUNDS_TO_KILOGRAMS


def convert_height_to_meters(height_feet, height_inches):
    """
    Convert height in feet and inches to meters.

    Args:
        height_feet (int): Feet portion of height.
        height_inches (int): Inches portion of height.

    Returns:
        float: Total height in meters.
    """
    total_inches = (height_feet * FEET_TO_INCHES) + height_inches
    return total_inches * INCHES_TO_METERS


# BMI Calculation
def calculate_bmi(weight_kilograms, height_meters):
    """
    Calculate BMI using the metric formula:
        BMI = weight_kg / (height_m ** 2)

    Args:
        weight_kilograms (float): Weight in kilograms.
        height_meters (float): Height in meters.

    Returns:
        float: Calculated BMI.
    """
    return weight_kilograms / (height_meters ** 2)


# Output Function
def display_bmi_results(bmi_value):
    """
    Display the BMI result formatted to one decimal place and show
    a legend with BMI categories.

    Args:
        bmi_value (float): Calculated BMI.
    """
    print(f"\nYour BMI is: {bmi_value:.1f}\n")
    print("BMI Category Legend:")
    print(f"  Underweight: less than {UNDERWEIGHT_THRESHOLD}")
    print(f"  Normal weight: {UNDERWEIGHT_THRESHOLD} to less than {OVERWEIGHT_THRESHOLD}")
    print(f"  Overweight: {OVERWEIGHT_THRESHOLD} or greater")


# Main Program
def main():
    """
    Main function to orchestrate input collection, conversions,
    BMI calculation, and output.
    """
    # Get user input
    weight_pounds = get_weight_pounds()
    height_feet = get_height_feet()
    height_inches = get_height_inches()

    # Convert to metric units
    weight_kilograms = convert_weight_to_kilograms(weight_pounds)
    height_meters = convert_height_to_meters(height_feet, height_inches)

    # Calculate BMI
    bmi_value = calculate_bmi(weight_kilograms, height_meters)

    # Display results
    display_bmi_results(bmi_value)


# Program entry point
if __name__ == "__main__":
    main()
