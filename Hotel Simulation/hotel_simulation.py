import concurrent.futures
import threading
import time
import datetime
import random
import logging

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M')

# Queues & Locks
Lock_Reception = threading.Lock()
Lock_Bellhops = threading.Lock()
Lock_room = threading.Lock()
Lock_restaurant = threading.Lock()
Lock_bar = threading.Lock()
Lock_checkout = threading.Lock()

bar_capacity = 50
guests_at_bar = 0

restaurant_capacity = 150
guests_at_restaurant = 0

# Shared Variables
available_receptionists = 6
available_bellhops = 5
available_housekeepers = 15

# Available Rooms
available_rooms = [f"{floor}{room:02d}" for floor in range(1, 4) for room in range(0, 11)]
random.shuffle(available_rooms)

# Guest Class
class Guest:
    """
    Represents a guest at the hotel.

    Attributes:
        guest_id (str): The unique ID of the guest.
        guest_name (str): The name of the guest.
        checkin_time (float): The time the guest checked in.
        checkout_time (float): The time the guest checked out.
        room_number (str): The room number assigned to the guest.
        has_luggage (bool): Indicates if the guest has luggage.
        luggage_handled (bool): Indicates if the guest's luggage has been handled.
        room_service_order (str): The room service order of the guest.
        room_service_time (float): The time the guest ordered room service.
        housekeeping_done (bool): Indicates if housekeeping has been done.
        housekeeping_time (float): The time housekeeping was done.
        room_service_done (bool): Indicates if room service has been done.
        room_service_arrival (float): The time room service arrived.
        time_in_hotel (float): The total time the guest spent in the hotel.
    """
    def __init__(self, guest_id, guest_name, has_luggage) -> None:
        self.guest_id = guest_id
        self.guest_name = guest_name
        self.checkin_time = 0
        self.checkout_time = 0
        self.room_number = None
        self.has_luggage = has_luggage
        self.luggage_handled = False
        self.room_service_order = None
        self.room_service_time = 0
        self.housekeeping_done = False
        self.housekeeping_time = 0
        self.room_service_done = False
        self.room_service_arrival = 0
        self.time_in_hotel = 0

    def __repr__(self):
        return f"ID: {self.guest_id}, Name: {self.guest_name}"

# Initialize Current Date and Year
date_now = datetime.datetime.now()
curr_year = date_now.year

# Guest Initialization Function
def guest_init(x):
    """
        Initializes a Guest object.

        Args:
            x (int): A unique integer for generating guest ID and name.

        Returns:
            Guest: An initialized Guest object with a unique ID, name, and luggage status.
        """
    return Guest(
        f"111-{x}-{curr_year}",
        f"GST{curr_year}{x}",
        random.choice([True, False]),
    )

# Guest Process Function
def guest_process(guest):
    """
        Processes a guest through various stages of their stay at the hotel.

        Stages include reservation, check-in, luggage handling, activities (restaurant, bar, room service, housekeeping), and checkout.

        Args:
            guest (Guest): The Guest object representing the guest being processed.

        Raises:
            Exception: Logs any exception that occurs during guest processing.
        """
    global available_receptionists
    global available_bellhops
    global available_housekeepers
    global bar_capacity
    global guests_at_bar
    global restaurant_capacity
    global guests_at_restaurant
    global available_rooms

    try:
        # Reservation
        while True:
            with Lock_Reception:
                if available_receptionists > 0:
                    available_receptionists -= 1
                    time.sleep(random.uniform(0.1, 0.2))
                    logging.info(f"{guest.guest_id}: has reserved the room.")
                    available_receptionists += 1
                    break
                else:
                    logging.info(f"No receptionist available! {guest.guest_id} is waiting for a receptionist.")
                    time.sleep(random.uniform(0.1, 0.2))

        # Check-in
        while True:
            with Lock_Reception:
                if available_receptionists > 0:
                    available_receptionists -= 1
                    time.sleep(random.uniform(0.1, 0.3))
                    if available_rooms:
                        guest.room_number = available_rooms.pop()
                        logging.info(f"{guest.guest_id}: has checked in, The room number is {guest.room_number}.")
                        guest.checkin_time = time.time()
                    else:
                        logging.info(f"No rooms available for {guest.guest_id}!")
                    available_receptionists += 1
                    break
                else:
                    logging.info(f"No receptionist available! {guest.guest_id} is waiting for a receptionist.")
                    time.sleep(random.uniform(0.1, 0.3))

        # Luggage Handling
        while True:
            with Lock_Bellhops:
                if available_bellhops > 0:
                    available_bellhops -= 1
                    if guest.has_luggage:
                        time.sleep(random.uniform(0.1, 0.5))
                        logging.info(f"{guest.guest_id}: Bellhop is carrying out the luggage.")
                        guest.luggage_handled = True
                    else:
                        logging.info(f"{guest.guest_id}: has no luggage.")
                        guest.luggage_handled = False
                    available_bellhops += 1
                    break
                else:
                    logging.info(f"No bellhops available! {guest.guest_id} is waiting for a bellhop.")
                    time.sleep(random.uniform(0.1, 0.3))

        # Guest Activity
        while True:
            option = random.randint(1, 4)
            if option == 1:
                # Restaurant
                with Lock_restaurant:
                    if guests_at_restaurant < restaurant_capacity:
                        guests_at_restaurant += 1
                        logging.info(f"{guest.guest_id}: has entered the restaurant.")
                        time.sleep(random.uniform(0.1, 0.5))
                        guests_at_restaurant -= 1
                        break
                    else:
                        logging.info(f"Restaurant is full! {guest.guest_id} is waiting or choosing another option.")
                        continue
            elif option == 2:
                # Bar
                with Lock_bar:
                    if guests_at_bar < bar_capacity:
                        guests_at_bar += 1
                        logging.info(f"{guest.guest_id}: has entered the bar.")
                        time.sleep(random.uniform(0.1, 0.5))
                        guests_at_bar -= 1
                        break
                    else:
                        logging.info(f"Bar is full! {guest.guest_id} is waiting or choosing another option.")
                        continue
            elif option == 3:
                # Room Service
                with Lock_room:
                    if available_housekeepers > 0:
                        available_housekeepers -= 1
                        logging.info(f"{guest.guest_id}: has ordered room service.")
                        guest.room_service_order = random.choice(['breakfast', 'cleaning', 'laundry'])
                        time.sleep(random.uniform(0.1, 0.5))
                        available_housekeepers += 1
                        break
                    else:
                        logging.info(f"{guest.guest_id}: is waiting for a housekeeper to be available.")
                        time.sleep(random.uniform(0.1, 0.3))
            else:
                # Housekeeping
                with Lock_room:
                    if available_housekeepers > 0:
                        available_housekeepers -= 1
                        logging.info(f"{guest.guest_id}: requested housekeeping.")
                        time.sleep(random.uniform(0.1, 0.5))
                        available_housekeepers += 1
                        break
                    else:
                        logging.info(f"{guest.guest_id}: waiting for housekeeper to be available.")
                        time.sleep(random.uniform(0.1, 0.3))

        # Checkout
        while True:
            with Lock_checkout:
                logging.info(f"{guest.guest_id}: is checking out.")
                if guest.luggage_handled:
                    time.sleep(random.uniform(0.1, 0.5))
                    logging.info(f"{guest.guest_id}: Bellhop is carrying out the luggage.")
                guest.checkout_time = time.time()
                guest.time_in_hotel = guest.checkout_time - guest.checkin_time
                break
    except Exception as e:
        logging.error(f"Error processing guest {guest.guest_id}: {e}")



# Simulation Execution
"""
    Executes the guest processing simulation with a specified number of threads.

    Initializes a list of Guest objects and maps them to the guest_process function using a ThreadPoolExecutor.
    """
with concurrent.futures.ThreadPoolExecutor(max_workers=400) as executor:
    guests = [guest_init(i) for i in range(1, 401)]
    executor.map(guest_process, guests)

logging.info("Simulation completed.")
