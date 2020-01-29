from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
graph = {}

# attempts = []


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


def add_room():
    room = {}
    for i in player.current_room.get_exits():
        room[i] = '?'
    graph[player.current_room.id] = room


def valid_direction(room):
    options = []
    current_direction = None
    for direction in graph[room.id]:
        if graph[room.id][direction] == '?':
            options.append(direction)
    if len(traversal_path) > 0:
        current_direction = traversal_path[-1]
    if len(options) > 0:
        return random.choice(options)
        if current_direction in options:
            return current_direction
        else:
            return random.choice(options)
    else:
        return None

opposite_direction = {'s':'n', 'n':'s', 'e':'w', 'w':'e'}

def convert_path(path):
    room_ids = []
    directions = []
    next_room = None
    for room in path:
        room_ids.append(room.id)

    for i, room_id in enumerate(room_ids):
        if i < len(room_ids) - 1:
            next_room = room_ids[i+1]
        direction = [dir for dir, room in graph[room_id].items()
                     if room == next_room]
        if len(direction) > 0:
            directions.append(direction[0])
    return directions


def find_shortest_path(starting_room):
    queue = Queue()
    queue.enqueue([starting_room])
    visited = set()
    while queue.size() > 0:
        path = queue.dequeue()
        room = path[-1]
        if valid_direction(room) is not None:
            return convert_path(path)
        if room.id not in visited:
            visited.add(room.id)
            for direction in graph[room.id]:
                new_room = room.get_room_in_direction(direction)
                new_path = path + [new_room]
                queue.enqueue(new_path)


def traverse():
    if len(graph) == 0:
        add_room()

    while len(graph) < len(room_graph):
        original_room = player.current_room.id
        direction = valid_direction(player.current_room)

        if direction is not None:
            player.travel(direction)
            traversal_path.append(direction)
            graph[original_room][direction] = player.current_room.id

            if player.current_room.id not in graph:
                add_room()
                graph[player.current_room.id][opposite_direction[direction]] = original_room

        else:
            path = find_shortest_path(player.current_room)
            for d in path:
                player.travel(d)
                traversal_path.append(d)



# def best_path(traversal_path):
#     print("INITIAL", traversal_path)
#     while len(traversal_path) > 960:
#       # need to reset the position to room 0
#         traversal_path = []
#         traverse()
#         print("TEST", traversal_path)

#     return traversal_path

# print("BEST", best_path(traversal_path))

# traversal_path = best_path(traversal_path)
traverse()


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
