# Hotel Guest Simulation
This project simulates the behavior of guests in a hotel environment using multithreading in Python. Each guest performs tasks such as checking in, handling luggage, visiting the restaurant or bar, ordering room service, and checking out. The simulation records the behavior and time spent on each task.


## Features
- Simulates multiple guests performing different activities concurrently.
- Tracks and records the time spent by each guest on their activities.
- Generates a report of the simulation, detailing the activities and the total time spent by each guest.

## Classes and Methods
- **Guest Class**: Represents a guest at the hotel with attributes including:
    - Unique ID
    - Name
    - Check-in time
    - Check-out time
    - Room number
    - Luggage status
    - Luggage handling status
    - Room service order and time
    - Housekeeping status and time
    - Total time spent in the hotel

- **Guest Initialization Function**: Initializes a Guest object with a unique ID, name, and luggage status.
- **Guest Process Function**: Processes a guest through various stages of their stay at the hotel, including: Reservation, Check-in, Luggage handling, Activities (restaurant, bar, room service, housekeeping), Checkout.

## Simulation Execution
Executes the guest processing simulation using a specified number of threads. Initializes a list of Guest objects and processes them concurrently using a '**ThreadPoolExecutor**'.

## Running the Simulation
To run the simulation, create instances of the Guest class and process them using multithreading. This project simulates 400 guests and logs their activities. The log provides detailed insights into the hotel's operations and guest behavior. Adjust the number of guests and other parameters as needed to suit specific requirements. The simulation tracks and records the time spent by each guest on their activities, offering a comprehensive view of hotel operations.
