import threading
import random
import time
import pandas as pd

class Student:
    """
    Represents a student who can raise and lower their hand, and give a presentation.

    Attributes:
        id (int): The unique ID of the student.
        hand_raised (bool): Indicates if the student's hand is raised.
        has_presented (bool): Indicates if the student has presented.
    """
    def __init__(self, id):
        """
        Initializes a Student instance with a unique ID.

        Args:
            id (int): The unique ID of the student.
        """
        self.id = id
        self.hand_raised = False
        self.has_presented = False

    def raise_hand(self):
        """
        Raises the student's hand.
        """
        self.hand_raised = True
        print(f"Student {self.id} has raised their hand.")

    def lower_hand(self):
        """
        Lowers the student's hand.
        """
        self.hand_raised = False
        print(f"Student {self.id} has lowered their hand.")

    def present(self):
        """
        Simulates the student giving a presentation for 5 seconds.
        """
        self.hand_raised = False
        self.has_presented = True
        print(f"Student {self.id} is presenting.")
        time.sleep(5)
        print(f"Student {self.id} has finished presenting.")

class Teacher:
    """
    Represents a teacher who calls on students to present.

    Attributes:
        id (int): The unique ID of the teacher.
        students (list): The list of students in the class.
    """
    def __init__(self, id, students, stop_event):
        """
        Initializes a Teacher instance with a unique ID and a list of students.

        Args:
            id (int): The unique ID of the teacher.
            students (list): The list of students in the class.
            stop_event (threading.Event): Event to signal when to stop the simulation.
        """
        self.id = id
        self.students = students
        self.stop_event = stop_event

    def call_on_student(self):
        """
        Calls on students to present, prioritizing those with raised hands. Stops when all students have presented or the stop event is set.
        """
        while not self.stop_event.is_set():
            random.shuffle(self.students)
            for student in self.students:
                if student.hand_raised:
                    student.present()
                    break
            else:
                for student in self.students:
                    if not student.has_presented:
                        student.present()
                        break
            time.sleep(1)

def student_behavior(student, stop_event):
    """
    Simulates the behavior of a student, randomly raising and lowering their hand.

    Args:
        student (Student): The student whose behavior is being simulated.
        stop_event (threading.Event): Event to signal when to stop the simulation.
    """
    while not student.has_presented and not stop_event.is_set():
        if random.random() < 0.1:
            student.raise_hand()
        if random.random() < 0.05:
            student.lower_hand()
        time.sleep(random.uniform(1, 3))

def print_report(students):
    """
    Prints a report of which students have presented, who raised their hands, and who did not present.

    Args:
        students (list): The list of students in the class.
    """
    raised_hands_students = [student.id for student in students if student.hand_raised]
    presented_students = [student.id for student in students if student.has_presented]
    not_presented_students = [student.id for student in students if not student.has_presented]

    max_length = max(len(raised_hands_students), len(presented_students), len(not_presented_students))
    raised_hands_students.extend([''] * (max_length - len(raised_hands_students)))
    presented_students.extend([''] * (max_length - len(presented_students)))
    not_presented_students.extend([''] * (max_length - len(not_presented_students)))

    report_df = pd.DataFrame({
        'Raised Hands': raised_hands_students,
        'Presented': presented_students,
        'Not Presented': not_presented_students
    })

    print("\nPresentation Report:")
    print(report_df.to_string(index=False))

def stop_simulation_after_timeout(stop_event, timeout):
    """
    Stops the simulation after a specified timeout.

    Args:
        stop_event (threading.Event): Event to signal when to stop the simulation.
        timeout (int): The time in seconds after which the simulation should stop.
    """
    time.sleep(timeout)
    stop_event.set()

students = [Student(i) for i in range(1, 51)]
stop_event = threading.Event()
teachers = [Teacher(1, students, stop_event), Teacher(2, students, stop_event)]

student_threads = [threading.Thread(target=student_behavior, args=(student, stop_event)) for student in students]
teacher_threads = [threading.Thread(target=teacher.call_on_student) for teacher in teachers]

# Start a thread to stop the simulation after 60 seconds
timeout_thread = threading.Thread(target=stop_simulation_after_timeout, args=(stop_event, 60))
timeout_thread.start()

for thread in student_threads + teacher_threads:
    thread.start()

for thread in student_threads + teacher_threads:
    thread.join()

timeout_thread.join()

print_report(students)
