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
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

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
    for direction in graph[room.id]:
        if graph[room.id][direction] == '?':
            options.append(direction)
    return random.choice(options)


def opposite_direction(direction):
    if direction == 's':
        return 'n'
    elif direction == 'n':
        return 's'
    elif direction == 'e':
        return 'w'
    elif direction == 'w':
        return 'e'


def find_shortest_path():
    pass


def traverse():
    if len(graph) == 0:
        add_room()
    # while len(graph) < len(room_graph):
    original_room = player.current_room.id
    direction = valid_direction(player.current_room)
    print(direction, "STARTS", player.current_room.id)
    player.travel(direction)
    graph[original_room][direction] = player.current_room.id
    print("ENDS", player.current_room.id)

    # if the room isn't in the graph, add it
    if player.current_room.id not in graph:
        add_room()
        graph[player.current_room.id][opposite_direction(
            direction)] = original_room

    print("TEST", graph[player.current_room.id][opposite_direction(direction)])
    print("OPPOSITE", opposite_direction('s'))
    print("EXITS", player.current_room.get_exits())
    # set opposite direction of current room to previous room

    # else find a new room with a valid room


traverse()
print("GRAPH", graph)
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
