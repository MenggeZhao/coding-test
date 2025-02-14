# Review 1

def add_to_list(value, my_list=[]):

    my_list.append(value)

    return my_list

 """
This function uses a mutable default argument, my_list=[]. It can cause messy results. When passing a mutable value as a default argument in a function, the default argument is changed anytime that value is mutated. This means the same list will be used across multiple function calls.

To solve the problem, use 'None' as a default. Then, assign the mutable value inside the function.

 """

def add_to_list_modified(value, my_list=None):
    
    if my_list is None:
        my_list = []

    my_list.append(value)

    return my_list
    
# Review 2

def format_greeting(name, age):

    return "Hello, my name is {name} and I am {age} years old."


"""
This function missed the correct coding format to add a variable string into another string. It should use f-string or .format() method to add {name} and {age} into the returning string.
"""

def format_greeting_modified(name, age):

    return f"Hello, my name is {name} and I am {age} years old."
 

# Review 3

class Counter:

    count = 0

 

    def __init__(self):

        self.count += 1

 

    def get_count(self):

        return self.count
    
"""
The variable 'self.count' inside __init__ does not initialize correctly.
self.count += 1 refers to an instance variable, but it is not initialized.
Since count is defined at the class level, all instances will share the same value.

"""
# if the 'count' will incremented every time an instance will created, the class should be modified


class Counter:
    count = 0  # Shared across all instances

    def __init__(self):
        self.count = Counter.count
        Counter.count += 1  # Modify the class variable

    def get_count(self):
        return self.count  # Return instance-level count
    
    def get_total_count(self):
        return Counter.count  # Return instance-level count
    
    
    
    
# Review 4

import threading

class SafeCounter:

    def __init__(self):

        self.count = 0

    def increment(self):
        self.count += 1


def worker(counter):

    for _ in range(1000):

        counter.increment()


counter = SafeCounter()

threads = []

for _ in range(10):

    t = threading.Thread(target=worker, args=(counter,))

    t.start()

    threads.append(t)


for t in threads:

    t.join()

"""
 Since multiple threads modify self.count without synchronization, race conditions may occur, leading to inconsistent values.
"""


import threading

class SafeCounter:
    def __init__(self):
        self.count = 0
         # Add a lock
        self.lock = threading.Lock() 

    def increment(self):
        # Ensure exclusive access
        with self.lock:  
            self.count += 1

def worker(counter):
    for _ in range(1000):
        counter.increment()

counter = SafeCounter()
threads = []
for _ in range(10):
    t = threading.Thread(target=worker, args=(counter,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

    
# Review 5

def count_occurrences(lst):

    counts = {}

    for item in lst:

        if item in counts:

            counts[item] =+ 1

        else:

            counts[item] = 1

    return counts

 """
 =+ 1 will raise an error before compileing the scripts. It should be += 1.
 
 """
    
def count_occurrences_modified(lst):
    counts = {}
    for item in lst:
        if item in counts:
             # Corrected
            counts[item] += 1 
        else:
            counts[item] = 1
    return counts