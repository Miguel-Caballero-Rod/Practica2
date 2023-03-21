"""
Solution to the one-way tunnel
"""
import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = 1
NORTH = 0

NCARS = 20
NPED = 5
TIME_CARS = 0.5  # a new car enters each 0.5s
TIME_PED = 1 # a new pedestrian enters each 5s
TIME_IN_BRIDGE_CARS = (1, 0.5) # normal 1s, 0.5s
TIME_IN_BRIDGE_PEDESTRGIAN = (30, 10) # normal 1s, 0.5s

class Monitor():
    def __init__(self):
        self.mutex = Lock()
        self.num_monitor = Value('i', 0)
        self.pueden_entrar_sur = Condition(self.mutex)
        self.num_norte = Value('i', 0)
        self.pueden_entrar_norte = Condition(self.mutex)
        self.num_sur = Value('i', 0)
        self.pueden_entrar_pedestrians = Condition(self.mutex)
        self.num_pedestrians = Value('i', 0)
        
    def nobody_from_north(self) -> bool:
        return self.num_norte.value == 0
    
    def nobody_from_south(self) -> bool:
        return self.num_sur.value == 0
    
    def no_pedestrians(self) -> bool:
        return self.num_pedestrians.value == 0
    
    def free_for_north(self) -> bool:
        return self.no_pedestrians() and self.nobody_from_south()
    
    def free_for_south(self) -> bool:
        return self.nobody_from_north() and self.no_pedestrians()
    
    def no_cars(self) -> bool:
        return self.nobody_from_north() and self.nobody_from_south()

    def wants_enter_car(self, direction: int) -> None:
        self.mutex.acquire()
        self.num_monitor.value += 1
        if direction == 1:
            self.pueden_entrar_sur.wait_for(self.free_for_south)
            self.num_sur.value += 1
        else:
            self.pueden_entrar_norte.wait_for(self.free_for_north)
            self.num_norte.value += 1
        self.mutex.release()

    def leaves_car(self, direction: int) -> None:
        self.mutex.acquire() 
        self.num_monitor.value += 1
        if direction == 1:
            self.num_sur.value -= 1
        else:
            self.num_norte.value -= 1
        if self.no_cars():
            self.pueden_entrar_pedestrians.notify_all()
        if self.free_for_south():
            self.pueden_entrar_sur.notify_all()
        if self.free_for_north():
            self.pueden_entrar_norte.notify_all()
        self.mutex.release()

    def wants_enter_pedestrian(self) -> None:
        self.mutex.acquire()
        self.num_monitor.value += 1
        self.pueden_entrar_pedestrians.wait_for(self.no_cars)
        self.num_pedestrians.value += 1
        self.mutex.release()

    def leaves_pedestrian(self) -> None:
        self.mutex.acquire() 
        self.num_monitor.value += 1
        self.num_pedestrians.value -= 1
        if self.no_cars():
            self.pueden_entrar_pedestrians.notify_all()
        if self.free_for_south():
            self.pueden_entrar_sur.notify_all()
        if self.free_for_north():
            self.pueden_entrar_norte.notify_all()
        self.mutex.release()
        
    def __repr__(self) -> str:   # para mostrar el monitor por pantalla
        return f'Monitor: {self.num_monitor.value}'

def delay_car_north(factor=1) -> None:
    time.sleep(random.random()/factor)

def delay_car_south(factor=1) -> None:
    time.sleep(random.random()/factor)
    
def delay_pedestrian(factor=1) -> None:
    time.sleep(random.random()/factor)

def car(cid: int, direction: int, monitor: Monitor)  -> None:
    print(f"car {cid} heading {direction} wants to enter. {monitor}")
    monitor.wants_enter_car(direction)
    print(f"car {cid} heading {direction} enters the bridge. {monitor}")
    if direction==NORTH :
        delay_car_north()
    else:
        delay_car_south()
    print(f"car {cid} heading {direction} leaving the bridge. {monitor}")
    monitor.leaves_car(direction)
    print(f"car {cid} heading {direction} out of the bridge. {monitor}")

def pedestrian(pid: int, monitor: Monitor) -> None:
    print(f"pedestrian {pid} wants to enter. {monitor}")
    monitor.wants_enter_pedestrian()
    print(f"pedestrian {pid} enters the bridge. {monitor}")
    delay_pedestrian()
    print(f"pedestrian {pid} leaving the bridge. {monitor}")
    monitor.leaves_pedestrian()
    print(f"pedestrian {pid} out of the bridge. {monitor}")



def gen_pedestrian(monitor: Monitor) -> None:
    pid = 0
    plst = []
    for _ in range(NPED):
        pid += 1
        p = Process(target=pedestrian, args=(pid, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1/TIME_PED))

    for p in plst:
        p.join()

def gen_cars(monitor) -> Monitor:
    cid = 0
    plst = []
    for _ in range(NCARS):
        direction = NORTH if random.randint(0,1)==1  else SOUTH
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1/TIME_CARS))

    for p in plst:
        p.join()

def main():
    monitor = Monitor()
    gcars = Process(target=gen_cars, args=(monitor,))
    gped = Process(target=gen_pedestrian, args=(monitor,))
    gcars.start()
    gped.start()
    gcars.join()
    gped.join()
    

if __name__ == '__main__':
    main()
