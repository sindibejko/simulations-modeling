# Classroom Simulation
This project simulates a classroom environment with 50 students and 2 teachers using multithreading in Python. Students randomly decide to raise their hands, and teachers call on students to give presentations. If no student has raised their hand, the teacher will call on a student they haven't called before. The simulation stops after a specified timeout, and a report is generated.

## Features
- Simulates 50 students randomly raising and lowering their hands.
- Two teachers call on students to give presentations.
- Each presentation lasts for 5 seconds.
- The simulation stops after a specified timeout (e.g., 60 seconds).
- Generates a report showing which students raised their hands, who presented, and who did not present.


## Classes and Methods
- **Student Class**: Represents a student who can raise and lower their hand and give a presentation.
- **Teacher Class**: Manages the process of calling on students to present, ensuring each student presents only once, and prioritizing those with raised hands.

To run the simulation, execute the script. This will start the student and teacher simulations, manage the interactions between students and teachers, and generate a report after the simulation stops.


## Additional Notes
- Students randomly decide to raise their hands with a probability of 10%.
- Students randomly decide to lower their hands with a probability of 5%.
- The simulation stops after the specified timeout (e.g., 60 seconds).
- The report includes three columns: students who raised their hands, students who presented, and students who did not present.
