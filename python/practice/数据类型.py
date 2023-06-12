import datetime
import zoneinfo
import calendar
import collections
import heapq
import bisect
import array
import weakref
import types
import copy
import pprint
import reprlib
import enum
import networkx as nx

# datetime
current_datetime = datetime.datetime.now()
print("Current datetime:", current_datetime)

# zoneinfo
timezone = zoneinfo.ZoneInfo("America/New_York")
print("Timezone:", timezone)

# calendar
cal = calendar.Calendar()
months = [month.strftime("%B") for month in cal.itermonthdates(2023, 1)]
print("Months:", months)

# collections
my_list = collections.deque([1, 2, 3])
my_list.append(4)
print("Deque:", my_list)

# heapq
heap = [1, 3, 2, 5, 4]
heapq.heapify(heap)
print("Heap:", heap)

# bisect
sorted_list = [1, 2, 4, 5]
index = bisect.bisect(sorted_list, 3)
print("Index:", index)

# array
my_array = array.array("i", [1, 2, 3])
print("Array:", my_array)

# weakref
class MyClass:
    pass

my_object = MyClass()
ref = weakref.ref(my_object)
print("Weak reference:", ref())

# types
MyClass = types.new_class("MyClass")
obj = MyClass()
print("Object type:", type(obj))

# copy
my_list = [1, [2, 3]]
shallow_copy = copy.copy(my_list)
deep_copy = copy.deepcopy(my_list)
print("Shallow copy:", shallow_copy)
print("Deep copy:", deep_copy)

# pprint
data = {"name": "John", "age": 30}
print("Pretty printed data:")
pprint.pprint(data)

# reprlib
long_string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
short_repr = reprlib.repr(long_string)
print("Short representation:", short_repr)

# enum
class Color(enum.Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

print("Color enum values:")
for color in Color:
    print(color)

# networkx graph
graph = nx.Graph()
graph.add_edge("A", "B")
graph.add_edge("B", "C")
print("Graph nodes:", graph.nodes())
print("Graph edges:", graph.edges())
