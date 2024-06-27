import threading
import random
import time
import concurrent.futures
import traceback

number_of_x_squares = 5
number_of_y_squares = 5
coordinate_dictionary = {}
for x in range(0, number_of_x_squares + 1):
    for y in range(0, number_of_y_squares + 1):
        coordinate_dictionary[(x, y)] = {
            "right_queue": [],
            "down_queue": [],
            "where_can_i_move": "right" if x % 3 == 0 else "down",
            "right_queue_lock": threading.Lock(),
            "down_queue_lock": threading.Lock(),
            "x": x,
            "y": y
        }


def flipping_semaphore(structure):
    """
    Simulates the flipping of a traffic light semaphore at a specific grid location.

    Args:
        structure (dict): The dictionary representing a specific grid location and its semaphore state.
    """
    try:
        while not is_the_program_over:
            print(f"The semaphore at x: {structure['x']} y: {structure['y']} is flipping")
            if structure["where_can_i_move"] == "right":
                structure["where_can_i_move"] = "down"
            else:
                structure["where_can_i_move"] = "right"
            time.sleep(random.randrange(3, 7))
    except Exception:
        traceback.print_exc()


def cars(id):
    """
    Simulates a car moving through the grid, queuing at traffic lights, and changing directions.

    Args:
        id (int): The unique ID of the car.
    """
    try:
        route = ""
        direction = random.randrange(1, 3)
        if direction == 1:
            route = "down"
            x, y = random.randrange(0, number_of_x_squares + 1), 0
        else:
            route = "right"
            x, y = 0, random.randrange(0, number_of_y_squares + 1)

        print(f"Car {id} is going on route: {route}")

        while x <= number_of_x_squares and y <= number_of_y_squares:
            print(f"Car {id} is moving from {x},{y}")

            change_criteria = random.randrange(1, 10)

            if change_criteria == 1:
                print(f"CAR {id} IS CHANGING DIRECTION.")
                if direction == 1:
                    route = "right"
                else:
                    route = "down"
            else:
                if route == "down":
                    dictionary = coordinate_dictionary[(x, y)]
                    dictionary["down_queue_lock"].acquire()
                    dictionary["down_queue"].append(id)
                    dictionary["down_queue_lock"].release()
                    print(f"Car {id} is in the {x, y} queue.")
                    while dictionary["where_can_i_move"] != "down":
                        time.sleep(1)
                    dictionary["down_queue_lock"].acquire()
                    dictionary["down_queue"].remove(id)
                    dictionary["down_queue_lock"].release()
                    print(f"Car {id} is out of the {x, y} queue.")
                    y += 1

                if route == "right":
                    dictionary = coordinate_dictionary[(x, y)]
                    dictionary["right_queue_lock"].acquire()
                    dictionary["right_queue"].append(id)
                    dictionary["right_queue_lock"].release()
                    print(f"Car {id} is in the {x, y} queue.")
                    while dictionary["where_can_i_move"] != "right":
                        time.sleep(1)
                    dictionary["right_queue_lock"].acquire()
                    dictionary["right_queue"].remove(id)
                    dictionary["right_queue_lock"].release()
                    print(f"Car {id} is out of the {x, y} queue.")
                    x += 1
                print(f"Car {id} arrived at {x},{y}")
                time.sleep(1.5)

    except Exception:
        traceback.print_exc()


is_the_program_over = False
amount_of_cars = 2
amount_of_semaphores = len(coordinate_dictionary.items())
with concurrent.futures.ThreadPoolExecutor(max_workers=amount_of_semaphores) as executor:
    executor.map(flipping_semaphore, coordinate_dictionary.values())
    with concurrent.futures.ThreadPoolExecutor(max_workers=amount_of_cars) as executor:
        executor.map(cars, range(amount_of_cars))
    is_the_program_over = True
