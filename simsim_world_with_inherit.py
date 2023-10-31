from collections import deque
import random


class CommonQueue:
    def __init__(self):
        self._entities = deque()

    def receive_entity(self, entity):
        self._entities.append(entity)

    def send_entity(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def __len__(self):
        return len(self._entities)


class Barack(CommonQueue):
    """Represents a queue of workers"""
    def __init__(self):
        """Initialize a queue for workers"""
        super().__init__()

    def send_entity(self):
        """Removes and returns the first worker from the queue,
           if there are any"""
        if len(self._entities) > 0:
            return self._entities.popleft()
        else:
            raise IndexError("Cannot dequeue a worker from an empty queue!")


class Lada(CommonQueue):
    """Represents a queue of food"""
    def __init__(self):
        """Initialize a queue for food"""
        super().__init__()

    def send_entity(self):
        """Removes and returns the first food item from the queue, 
           if there are any"""
        if len(self._entities) > 0:
            return self._entities.popleft()
        else:
            raise IndexError("Cannot dequeue food from an empty queue!")


class Lager(CommonQueue):
    """Represent a stack of storing products"""
    def __init__(self):
        super().__init__()
        """Initialize a stack for products"""
        self._entities = []

    def send_entity(self):
        """Removes and returns the last product item from the stack,
           if there are any"""
        if len(self._entities) > 0:
            return self._entities.pop()
        else:
            raise IndexError("Empty products stack!")


class Mat:
    """Represent the quality of food"""
    def __init__(self):
        """Initialize a random value between -10, 30 for the quality of food"""
        self._Mat_quality = random.randint(-10, 30)

    def get_mat_quality(self):
        """Returns the quality of the food"""
        return self._Mat_quality


class Arbetare:
    """Represent a worker with health and life status"""
    worker_id_counter = 1

    def __init__(self):
        """Initialize a worker with health starts at 100, indicate if the
           worker is a live or not starts as a live."""
        self._worker_health = 100
        self._worker_is_alive = True
        self._worker_id = Arbetare.worker_id_counter
        Arbetare.worker_id_counter += 1

    def get_life_health(self):
        """Returns the current health of the worker"""
        return self._worker_health

    def worker_is_alive(self):
        """Check if the worker is a live"""
        return self._worker_is_alive

    def get_worker_id(self):
        """Returns the current ID-number of the worker"""
        return self._worker_id


class Produkter:
    """Represent an empty product class"""
    def __init__(self):
        pass


class Destination:
    def __init__(self):
        self._from_destination1 = None
        self._to_destination1 = None
        self._workers_data = {}

    def set_from_destination1(self, from_destination1):
        self._from_destination1 = from_destination1

    def set_to_destination1(self, to_destination1):
        self._to_destination1 = to_destination1

    def check_workers(self, from_destination1):
        return from_destination1 is not None and from_destination1.__len__() > 0


class Fabrik(Destination):
    def __init__(self):
        super().__init__()
        self._to_destination2 = None
    
    def set_to_destination2(self, to_destination2):
        self._to_destination2 = to_destination2

    def check_address(self, from_destination1, to_destination2, to_destination1):
        return from_destination1 is not None and to_destination2 is not None and to_destination2 is not None

    def create_product(self):
        if self.check_address(self._from_destination1, self._to_destination2, self._to_destination1) and self.check_workers(self._from_destination1):  # Check if necessary destinations are set and workers are available
            worker1 = self._from_destination1.send_entity()  # Retrieve a worker from the source (_from_destination1)
            worker_id = worker1.get_worker_id()  # Get the ID of the worker
            if worker_id not in self._workers_data:
                self._workers_data[worker_id] = worker1.get_life_health()  # # If this worker is not already in the worker data(dict), add their ID and initial health
            health_of_worker1 = self._workers_data[worker_id]  # Get the worker's latest health data
            print(f"Worker {worker_id}'s health: {health_of_worker1}")
            accident = 40
            work_intensity = random.randint(40, 60)
            health_of_worker1 -= work_intensity
            print(f"Worker {worker_id}'s health after work: {health_of_worker1}")
            if health_of_worker1 <= 0:  # Check if the worker has died due to poor health
                worker1._worker_is_alive = False
                product = None  
                self._to_destination2.receive_entity(product)  
                print(f"The worker {worker_id} has died in the fabric. Number of workers left: {len(self._from_destination1)}")
            else:  # If the worker is alive, check if an accident occurs
                if random.randint(1, 100) <= accident:  # Check if an accident occurs (based on a random chance).
                    worker1._worker_is_alive = False  #  The worker dies
                    product = None
                    self._to_destination2.receive_entity(product)
                    print(f"The worker {worker_id} has died in an accident in the fabric. Number of workers left: {len(self._from_destination1)}")
                else:  # No accident 
                    product = Produkter()  # Create a product(Produkter)
                    self._to_destination2.receive_entity(product)  # Send the product to the storage (_to_destination2)
                    self._to_destination1.receive_entity(worker1)  # Send the worker back to the source for workers (_to_destination1)
                    print(f"A product has been created. Number of workers left: {len(self._from_destination1)}")
            self._workers_data[worker_id] = health_of_worker1  # Update the worker's health in the worker data


class Åker(Destination):
    def __init__(self):
        super().__init__()
        self._to_destination3 = None

    def set_to_destination3(self, to_destination3):
        self._to_destination3 = to_destination3

    def check_address(self, from_destination1, to_destination3, to_destination1):
        return from_destination1 is not None and to_destination3 is not None and to_destination1 is not None

    def produce_food(self):
        if self.check_address(self._from_destination1, self._to_destination3, self._to_destination1) and self.check_workers(self._from_destination1):
            worker1 = self._from_destination1.send_entity()  
            worker_id = worker1.get_worker_id()
            if worker_id not in self._workers_data:
                self._workers_data[worker_id] = worker1.get_life_health()
            health_of_worker1 = self._workers_data[worker_id]
            print(f"Worker {worker_id}'s health: {health_of_worker1}")
            accident = 40
            if random.randint(1, 100) <= accident:  
                health_of_worker1 -= random.randint(40, 60)
                print(f"Worker {worker_id}'s health after accident in field is: {health_of_worker1}")
                if health_of_worker1 <= 0:
                    worker1._worker_is_alive = False
                    food = None
                    self._to_destination3.receive_entity(food)
                    print(f"The worker {worker_id} has died in the field. Number of workers left is: {len(self._from_destination1)}")
                else:
                    food = Mat()
                    self._to_destination3.receive_entity(food)
                    self._to_destination1.receive_entity(worker1)
                    print(f"Food has been produced.  Number of workers left: {len(self._from_destination1)}")
            else:
                food = Mat()
                self._to_destination3.receive_entity(food)
                self._to_destination1.receive_entity(worker1)
                print(f"Food has been produced and there are no accident!. Number of workers left: {len(self._from_destination1)}")
            self._workers_data[worker_id] = health_of_worker1


class Matsal(Destination):
    def __init__(self):
        super().__init__()
        self._from_destination2 = None
    
    def set_from_destination2(self, from_destination2):
        self._from_destination2 = from_destination2

    def check_address(self, from_destination1, from_destination2, to_destination1):
        return from_destination1 is not None and from_destination2 is not None and to_destination1 is not None

    def check_food(self, from_destination2):
        return from_destination2 is not None and from_destination2.__len__() > 0

    def start_eating(self):
        if self.check_address(self._from_destination1, self._from_destination2, self._to_destination1) and \
           self.check_workers(self._from_destination1) and self.check_food(self._from_destination2):
            worker1 = self._from_destination1.send_entity()
            food = self._from_destination2.send_entity()
            worker_id = worker1.get_worker_id()
            if worker_id not in self._workers_data:
                self._workers_data[worker_id] = worker1.get_life_health()
            health_of_worker1 = self._workers_data[worker_id]
            if food is not None:
                if food.get_mat_quality() > 0:
                    if health_of_worker1 < 100:
                        health_increase = min(100 - health_of_worker1, food.get_mat_quality())
                        health_of_worker1 += health_increase
                        print(f"Worker {worker_id} gains {health_increase} health while eating. Worker's health after eating: {health_of_worker1}")
                elif food.get_mat_quality() < 0:
                    health_decrease = -food.get_mat_quality()
                    health_of_worker1 -= health_decrease
                    print(f"Worker {worker_id} loses {health_decrease} health due to bad food. Worker's health after eating: {health_of_worker1}")
                    if health_of_worker1 <= 0:
                        worker1._worker_is_alive = False
                        print(f"The worker {worker_id} has died in the matsal due to bad food. Number of workers left: {len(self._from_destination1)}")
                else:
                    print(f"Worker {worker_id} finishes eating. No change in health.")
            else:
                print(f"Worker {worker_id} starts eating, but there is no food available.")
            self._to_destination1.receive_entity(worker1)
            self._workers_data[worker_id] = health_of_worker1


class Hem(Destination):
    def __init__(self):
        super().__init__()
        self._from_destination4 = None
    
    def set_from_destination4(self, from_destination4):
        self._from_destination4 = from_destination4

    def check_address(self, from_destination1, from_destination4, to_destination1):
        return from_destination1 is not None and from_destination4 is not None and to_destination1 is not None

    def check_product(self, from_destination4):
        return from_destination4 is not None and from_destination4.__len__() > 0

    def set_home(self):
        used_products = []
        random_choice = random.choice([1, 2])
        if random_choice == 1:
            if self.check_address(self._from_destination1, self._from_destination4, self._to_destination1) and \
               self.check_workers(self._from_destination1) and self.check_product(self._from_destination4):
                worker1 = self._from_destination1.send_entity()
                product = self._from_destination4.send_entity()
                used_products.append(product)
                worker_id = worker1.get_worker_id()
                if worker_id not in self._workers_data:
                    self._workers_data[worker_id] = worker1.get_life_health()
                health_of_worker1 = self._workers_data[worker_id]
                print(f"Worker {worker_id} is at home alone. Worker's health before resting: {health_of_worker1}")
                if health_of_worker1 < 100:
                    health_increase = min(100 - health_of_worker1, random.randint(1, 10))
                    health_of_worker1 += health_increase
                    print(f"Worker {worker_id} gains {health_increase} health while resting at home. Worker's health after resting: {health_of_worker1}")
                self._to_destination1.receive_entity(worker1)
                self._workers_data[worker_id] = health_of_worker1
        if random_choice == 2:
            if self.check_address(self._from_destination1, self._from_destination4, self._to_destination1) and \
               self.check_workers(self._from_destination1) and self.check_product(self._from_destination4):
                if self._from_destination1.__len__() >= 2:
                    worker1 = self._from_destination1.send_entity()
                    worker2 = self._from_destination1.send_entity()
                    product = self._from_destination4.send_entity()
                    used_products.append(product)
                    worker_id1 = worker1.get_worker_id()
                    worker_health_1 = worker1.get_life_health()
                    worker_id2 = worker2.get_worker_id()
                    worker_health_2 = worker2.get_life_health()
                    print(f"Worker {worker_id1} with health {worker_health_1} and Worker {worker_id2} with health {worker_health_2} are at home. They become three.")
                    worker3 = Arbetare()
                    self._to_destination1.receive_entity(worker1)
                    self._to_destination1.receive_entity(worker2)
                    self._to_destination1.receive_entity(worker3)
                    print(f"Worker {worker3.get_worker_id()} is created.")
                    print(f"Number of workers left:{len(self._from_destination1)} ")
                else:
                    worker1 = self._from_destination1.send_entity()
                    product = self._from_destination4.send_entity()
                    used_products.append(product)
                    worker_id = worker1.get_worker_id()
                    if worker_id not in self._workers_data:
                        self._workers_data[worker_id] = worker1.get_life_health()
                    health_of_worker1 = self._workers_data[worker_id]
                    print(f"Worker {worker_id} is at home alone. Worker's health before resting: {health_of_worker1}")
                    if health_of_worker1 < 100:
                        health_increase = min(100 - health_of_worker1, random.randint(1, 10))
                        health_of_worker1 += health_increase
                        print(f"Worker {worker_id} gains {health_increase} health while resting at home. Worker's health after resting: {health_of_worker1}")
                    self._to_destination1.receive_entity(worker1)
                    self._workers_data[worker_id] = health_of_worker1


if __name__ == "__main__":
    # # Create two instances of each class
    barack1 = Barack()
    barack2 = Barack()
    fabric = Fabrik()
    fabric2 = Fabrik()
    field = Åker()
    field2 = Åker()
    dining_room = Matsal()
    dining_room2 = Matsal()
    home = Hem()
    home2 = Hem()
    warehouse = Lager()
    warehouse2 = Lager()
    save_food = Lada()
    save_food2 = Lada()

    # Randomly add workers to the barracks
    for _ in range(5):
        choice = random.choice([barack1, barack2])
        choice.receive_entity(Arbetare())

    # Set the source and destinations for the factory, field, dining room, and home
    fabric.set_from_destination1(barack1)
    fabric.set_to_destination2(warehouse)
    fabric.set_to_destination1(barack2)

    fabric2.set_from_destination1(barack2)
    fabric2.set_to_destination2(warehouse2)
    fabric2.set_to_destination1(barack1)

    field.set_from_destination1(barack1)
    field.set_to_destination3(save_food)
    field.set_to_destination1(barack2)

    field2.set_from_destination1(barack2)
    field2.set_to_destination3(save_food2)
    field2.set_to_destination1(barack1)

    dining_room.set_from_destination1(barack1)
    dining_room.set_from_destination2(save_food)
    dining_room.set_to_destination1(barack2)

    dining_room2.set_from_destination1(barack2)
    dining_room2.set_from_destination2(save_food2)
    dining_room2.set_to_destination1(barack1)

    home.set_from_destination1(barack1)
    home.set_from_destination4(warehouse)
    home.set_to_destination1(barack2)

    home2.set_from_destination1(barack2)
    home2.set_from_destination4(warehouse2)
    home2.set_to_destination1(barack1)

    # Run the simulation as long as there are workers in any barracks
    while len(barack1) > 0 or len(barack2) > 0:
        print("\n", "--------------------------")
        print(f"len barack 1: {len(barack1)}")
        print(f"len barack 2: {len(barack2)}")
        print("--------------------------", "\n")
        fabric.create_product()
        fabric2.create_product()
        field.produce_food()
        field2.produce_food()
        dining_room.start_eating()
        dining_room2.start_eating()
        home.set_home()
        home2.set_home()