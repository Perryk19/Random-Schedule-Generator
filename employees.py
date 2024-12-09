# Employee class definition
class Employee:
    def __init__(self, name):
        self.name = name
        self.id = id(self)
        self.availability = {}

# Function to load employees from a text file
def load_employees():
    try:
        employees = []
        with open("employees.txt", "r") as file:
            for line in file:
                # Parsing each line for employee data
                data = line.strip().split(",")
                name = data[0]
                availability = {data[i]: data[i + 1] for i in range(1, len(data), 2)}
                emp = Employee(name)
                emp.availability = availability
                employees.append(emp)
        return employees
    except FileNotFoundError:
        return []

# Function to save employees to a text file
def save_employees(employees):
    with open("employees.txt", "w") as file:
        for emp in employees:
            availability = []
            for day, times in emp.availability.items():
                for time in times:
                    availability.append(f"{day},{time}")
            file.write(f"{emp.name},{','.join(availability)}\n")

# Function to input employees and their availability
def input_employees():
    # Load existing employees if available
    employees = load_employees()

    while True:
        name = input("Enter the employee's first name (or 'done' to finish): ").strip().lower()
        if name == "done":
            break
        employee = Employee(name)

        print("\nEnter availability for each day of the week.")
        days_of_week = ["Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"]

        for day in days_of_week:
            while True:
                available = input(f"Is {name} available on {day}? (Y/N): ").strip().lower()
                if available not in ["y", "n"]:
                    print("Invalid input. Please enter 'Y' or 'N'.")
                    continue
                if available == "y":
                    selected_times = set()  # Track selected times for this day
                    while True:
                        print("\nAvailable times: Morning, Mid, Evening")
                        print("You can type 'ALL' to select all times or add one time at a time.")
                        time = input(f"When is {name} available on {day}? ").strip().lower()

                        if time == "all":
                            selected_times.update(["morning", "mid", "evening"])
                            break
                        elif time in ["morning", "mid", "evening"]:
                            if time in selected_times:
                                print(f"{time.capitalize()} has already been selected for {day}. Please choose a different time.")
                            else:
                                selected_times.add(time)
                                print(f"{time.capitalize()} added for {day}.")
                        else:
                            print("Invalid input. Please choose from Morning, Mid, Evening, or ALL.")
                        
                        # Ask if they want to add more times or stop
                        while True:
                            more = input("Do you want to add another time for this day? (Y/N): ").strip().lower()
                            if more in ["y", "n"]:
                                break
                            print("Invalid input. Please enter 'Y' or 'N'.")  # Error message for invalid input
                        
                        if more == "n":
                            break
                    
                    # Assign the selected times to the employee's availability
                    employee.availability[day] = list(selected_times)
                break

        employees.append(employee)

    # Save the employee data
    save_employees(employees)
    print("\nEmployee data saved successfully.")

# Run the employee input function
if __name__ == "__main__":
    input_employees()
