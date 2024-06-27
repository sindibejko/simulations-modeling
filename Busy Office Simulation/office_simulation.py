import threading
import random
import time
import concurrent.futures
import traceback
import pandas as pd

class Employee:
    """
    Represents an employee performing various tasks in a simulated office environment.

    Attributes:
        employee_id (int): The unique ID of the employee.
        task (str): The task assigned to the employee.
        time_spent (int): The time the employee spends on the task.
        simulator (Simulator): The simulator instance managing the simulation.
    """
    def __init__(self, employee_id, simulator):
        """
        Initializes an Employee instance with a unique ID, assigned task, and time spent on the task.

        Args:
            employee_id (int): The unique ID of the employee.
            simulator (Simulator): The simulator instance managing the simulation.
        """
        self.employee_id = employee_id
        self.task = random.choice(["Typing on a computer", "Making phone calls", "Taking breaks"])
        self.time_spent = random.randint(1, 10)
        self.simulator = simulator

    def start(self):
        """
        Simulates the employee performing their task for a random amount of time.
        After completing the task, the employee adds themselves to the simulator's queue.
        """
        try:
            print(f"Employee {self.employee_id} is {self.task}.")
            time.sleep(self.time_spent)
            print(f"Employee {self.employee_id} finished their task after {self.time_spent} hours.")
            self.simulator.addEmployeeToQueue(self)
        except Exception:
            traceback.print_exc()

class Simulator:
    """
    Manages the simulation of the office environment, including the behavior of multiple employees.

    Attributes:
        num_employees (int): The number of employees in the simulation.
        employee_queue (list): The queue of employees in the simulation.
        queue_lock (threading.Lock): A lock for synchronizing access to the employee queue.
        report_lock (threading.Lock): A lock for synchronizing access to the final report.
        final_report (dict): A dictionary storing the behavior and time spent by each employee.
    """
    def __init__(self, num_employees):
        """
        Initializes the Simulator instance with a specified number of employees.

        Args:
            num_employees (int): The number of employees in the simulation.
        """
        self.num_employees = num_employees
        self.employee_queue = []
        self.queue_lock = threading.Lock()
        self.report_lock = threading.Lock()
        self.final_report = {}

    def start(self):
        """
        Starts the simulation by creating a new thread for each employee.
        The threads are started concurrently, each simulating the behavior of a different employee.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_employees) as executor:
            self.employee_queue = [Employee(employee_id, self) for employee_id in range(1, self.num_employees + 1)]
            for i in self.employee_queue:
                executor.submit(i.start)

    def addEmployeeToQueue(self, employee):
        """
        Allows an employee to add themselves to the simulator's queue after completing their task.

        Args:
            employee (Employee): The employee adding themselves to the queue.
        """
        with self.report_lock:
            if employee.employee_id not in self.final_report:
                self.final_report[employee.employee_id] = [employee.task, employee.time_spent]

    def getReport(self):
        """
        Generates and prints a report of the simulation, including the behavior and time spent by each employee.
        The report includes a count of unique tasks and the total time spent on each task.
        """
        with self.report_lock:
            print("\nEmployee Report:\n")
            df = pd.DataFrame.from_dict(self.final_report, orient='index', columns=["Task", "Time Spent"])
            df.index.name = 'Employee ID'
            print(df.to_string(index=True, header=True))

            task_report = {"Typing on a computer": [0, 0], "Making phone calls": [0, 0], "Taking breaks": [0, 0]}
            for task, time_taken in self.final_report.values():
                task_report[task][0] += 1
                task_report[task][1] += time_taken

            print("\nTask Report:\n")
            columns = ["Task", "Amount of Employees", "Total Task Time"]
            values = []
            for task, info in task_report.items():
                amount_employees = info[0]
                total_time = info[1]
                values.append([task, amount_employees, total_time])
            df2 = pd.DataFrame(values, columns=columns)
            print(df2.to_string(index=False, header=True))

simulator = Simulator(5)
simulator.start()
simulator.getReport()
