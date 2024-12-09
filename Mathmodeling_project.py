'''
This code will allow the user to input an employee's information and
availability and will randimize a work schedule depending on number of check-ins
and check-out
'''
import random

# Employee class definition
class Employee:
    def __init__(self, name):
        self.name = name
        self.id = id(self)
        self.availability = {}

# Collect employee inputs
employees = []

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
                            break  # Valid input, exit the validation loop
                        print("Invalid input. Please enter 'Y' or 'N'.")  # Error message for invalid input
                    
                    if more == "n":
                        break
                
                # Assign the selected times to the employee's availability
                employee.availability[day] = list(selected_times)
            break

    employees.append(employee)

# Collect daily check-in and check-out data
days_of_week = ["Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"]
daily_checkins_outs = {}

for day in days_of_week:
    try:
        n_in = int(input(f"Enter the number of check-ins (n_in) for {day}: "))
        n_out = int(input(f"Enter the number of check-outs (n_out) for {day}: "))
        daily_checkins_outs[day] = (n_in, n_out)
    except ValueError:
        print("Invalid input. Please enter numeric values for check-ins and check-outs.")
        break

# Function to randomize the schedule
def randomize_schedule(employees, daily_checkins_outs):
    """
    Randomizes a work schedule for one week based on employee availability and daily check-in/out values.
    """
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

# Generate and print the schedule
weekly_schedule = randomize_schedule(employees, daily_checkins_outs)
print_schedule(weekly_schedule)
