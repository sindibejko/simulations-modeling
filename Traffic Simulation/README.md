# Traffic Simulation
This project simulates traffic flow on a 5x5 grid of roads with traffic lights, using multithreading in Python. Roads may have concurrent traffic lights, ensuring that intersecting roads do not have green lights simultaneously. Cars enter the grid, follow their route, and navigate through the traffic lights, queuing up as necessary. The simulation includes a mechanism to prevent cars from moving simultaneously through intersecting roads.

## Features
- Simulates multiple cars navigating a 5x5 grid of roads with traffic lights.
- Ensures traffic lights manage intersections to prevent concurrent green lights on intersecting roads.
- Cars can change direction and queue at traffic lights, advancing when the light turns green.
- Tracks the movement of each car and manages traffic flow efficiently.

## Classes and Methods
- **Traffic Light Simulator**: Simulates traffic lights at each intersection, changing between allowing cars to move "right" or "down" at random intervals.
- **Car Simulator**: Simulates cars moving through the grid, queuing at traffic lights, and following their route until they exit the grid or reach their destination.

To run the simulation, execute the script. This will start the traffic light and car simulations, managing the movement and interaction of cars within the grid.

## Additional Notes
- The simulation includes a mechanism to prevent cars from moving simultaneously through intersecting roads.
- Traffic lights flip their state at random intervals between 3 and 7 seconds.
- Cars can change direction randomly while navigating through the grid.

This project simulates multiple cars and generates a report of their activities.






