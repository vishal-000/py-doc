# daily_status.py

from datetime import datetime

def yes_no_input(prompt):
    while True:
        ans = input(prompt + " (y/n): ").strip().lower()
        if ans in ['y', 'n']:
            return "Yes" if ans == 'y' else "No"
        print("Please enter 'y' or 'n' only.")

def main():
    print("---- DAILY STATUS CHECK ----")

    # Checklist Inputs
    water = yes_no_input("Did you drink enough water today?")
    gym = yes_no_input("Did you go to the gym today?")
    productive_work = yes_no_input("Did you finish your productive work?")

    # Study hours
    while True:
        try:
            study_hours = float(input("How many hours did you study today? : "))
            break
        except ValueError:
            print("Enter a valid number.")

    # Prepare data to save
    date = datetime.now().strftime("%Y-%m-%d")
    entry = (
        f"Date: {date}\n"
        f"Water: {water}\n"
        f"Gym: {gym}\n"
        f"Study Hours: {study_hours}\n"
        f"Productive Work: {productive_work}\n"
        f"{'-'*40}\n"
    )

    # Save to a single file in Documents
    file_path = "/Users/vicky/Documents/daily_status"

    with open(file_path, "a") as file:
        file.write(entry)

    print(f"\nStatus saved successfully in: {file_path}")

if __name__ == "__main__":
    main()
