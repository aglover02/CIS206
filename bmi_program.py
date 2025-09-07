"""
BMI Calculator (Imperial to Metric)

This program prompts the user to enter their weight in pounds,
and their height in feet and inches. It then calculates the
Body Mass Index (BMI) using the imperial formula:

    BMI = (weight_lbs / (total_height_in)**2) * 703

The calculated BMI is displayed to one decimal place. A legend
shows standard BMI categories (underweight, normal, overweight)
based on WHO definitions.

BMI categories:
  Underweight: BMI < 18.5 kg/m²
  Normal weight: 18.5 ≤ BMI < 25.0 kg/m²
  Overweight: BMI ≥ 25.0 kg/m²
"""

# Constants for BMI category thresholds (kg/m^2)
UNDERWEIGHT_THRESHOLD = 18.5
OVERWEIGHT_THRESHOLD = 25.0

def get_user_input():
    """
    Prompt user to enter weight in pounds, then height in feet and inches.
    Returns a tuple: (weight_lbs, height_feet, height_inches).
    """
    weight_lbs = float(input("Enter your weight in pounds: "))
    height_feet = int(input("Enter your height - feet component: "))
    height_inches = int(input("Enter your height - inches component: "))
    return weight_lbs, height_feet, height_inches

def calculate_bmi(weight_lbs, height_feet, height_inches):
    """
    Calculate BMI using imperial units.
    
    Converts height in feet and inches to total inches, then applies:
        BMI = (weight_lbs / (height_in_inches ** 2)) * 703
    
    Returns BMI as a float.
    """
    total_height_inches = height_feet * 12 + height_inches
    bmi = (weight_lbs / (total_height_inches ** 2)) * 703
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
    Main function to run the BMI calculator program.
    """
    weight_lbs, height_feet, height_inches = get_user_input()
    bmi_result = calculate_bmi(weight_lbs, height_feet, height_inches)
    display_bmi_and_legend(bmi_result)

if __name__ == "__main__":
    main()
