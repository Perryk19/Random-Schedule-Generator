import random

# Employee class for managing employee details
class Employee:
    def __init__(self, emp_id, name):
        self.id = emp_id
        self.name = name
        self.availability = {}

    def add_availability(self, day, times):
        self.availability[day] = times

    def __str__(self):
        return f"{self.name}: {self.availability}"

# Function to load employees from a file (can be extended for text or CSV files)
def load_employees():
    try:
        with open("employees.txt", "r") as file:
            employees = []
            for line in file:
                data = line.strip().split(",")
                emp_id = int(data[0])
                name = data[1]
                availability = {data[i]: data[i+1] for i in range(2, len(data), 2)}  # Assuming format day,time pairs
                emp = Employee(emp_id, name)
                emp.availability = availability
                employees.append(emp)
            return employees
    except FileNotFoundError:
        print("No employee data found. Please add employees first.")
        return []

# Function to save employees to a file
def save_employees(employees):
    with open("employees.txt", "w") as file:
        for emp in employees:
            availability = [f"{day},{times}" for day, times in emp.availability.items()]
            file.write(f"{emp.id},{emp.name},{','.join(availability)}\n")

# Function to randomize the schedule
def randomize_schedule(employees, daily_checkins_outs):
    schedule = {day: {"Morning": [], "Mid": [], "Evening": []} for day in daily_checkins_outs.keys()}
    max_days_per_employee = 5
    employee_workdays = {emp.id: 0 for emp in employees}

    for day, shifts in schedule.items():
        n_in, n_out = daily_checkins_outs[day]
        morning_workers = 2 if n_in > 70 else random.randint(1, 2)
        evening_workers = 2 if n_out > 70 else random.randint(1, 2)

        for shift, workers_needed in [("Morning", morning_workers), ("Mid", 1), ("Evening", evening_workers)]:
            available_employees = [
                emp for emp in employees
                if day in emp.availability and shift.lower() in emp.availability[day]
                and employee_workdays[emp.id] < max_days_per_employee
            ]
            if available_employees:
                selected_workers = random.sample(available_employees, min(workers_needed, len(available_employees)))
                shifts[shift].extend([worker.name.capitalize() for worker in selected_workers])
                for worker in selected_workers:
                    employee_workdays[worker.id] += 1

    return schedule

# Function to print the schedule
def print_schedule(schedule):
    print("\nWeekly Work Schedule:")
    for day, shifts in schedule.items():
        print(f"\n{day}:")
        for shift, workers in shifts.items():
            workers_list = ', '.join(workers) if workers else "No workers assigned"
            print(f"  {shift}: {workers_list}")

# Main program for schedule management
if __name__ == "__main__":
    employees = load_employees()
    if not employees:
        exit()

    while True:
        print("\n1. Add Employees")
        print("2. Remove Employees")
        print("3. Generate Schedule")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            from employee_input import input_employees
            input_employees()
            employees = load_employees()  # Reload employees
        elif choice == "2":
            print("\nEmployees:")
            for i, emp in enumerate(employees):
                print(f"{i + 1}. {emp.name.capitalize()}")

            try:
                to_remove = int(input("Enter the number of the employee to remove: ")) - 1
                if 0 <= to_remove < len(employees):
                    removed = employees.pop(to_remove)
                    save_employees(employees)
                    print(f"Removed {removed.name.capitalize()} successfully.")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == "3":
            daily_checkins_outs = {}
            days_of_week = ["Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"]
            for day in days_of_week:
                try:
                    n_in = int(input(f"Enter the number of check-ins (n_in) for {day}: "))
                    n_out = int(input(f"Enter the number of check-outs (n_out) for {day}: "))
                    daily_checkins_outs[day] = (n_in, n_out)
                except ValueError:
                    print("Invalid input. Please enter numeric values for check-ins and check-outs.")
                    break

            schedule = randomize_schedule(employees, daily_checkins_outs)
            print_schedule(schedule)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")
