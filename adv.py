# from room import Room
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
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()



############ CODE BEGIN


player = Player(world.starting_room)

traversal_path = []
visited = {}
t_around = []
b_track = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

visited[player.current_room.id] = player.current_room.get_exits()   #add fst room and exits

while len(visited) < len(room_graph):                               # visited is less then length of rooms
    if player.current_room.id not in visited:                       # not visited
        visited[player.current_room.id] = player.current_room.get_exits() # add room and exits
        previous_direction = t_around[-1]                           # turn around
        visited[player.current_room.id].remove(previous_direction)  # remove from unexplored rooms

    if len(visited[player.current_room.id]) == 0:                   # if 0 all paths were examined in room(area)
        previous_direction = t_around[-1]                           # go back until new room found and assign
        t_around.pop()                                              # pop of room
        traversal_path.append(previous_direction)                   # add to the traverses path
        player.travel(previous_direction)                           # travel in that direction

    else:                                                           # explore new direction
        direction = visited[player.current_room.id][-1]             # go in the first direction found
        visited[player.current_room.id].pop()                       # pop from list
        traversal_path.append(direction)                            # add direction
        t_around.append(b_track[direction])                         # record opposite direction to t_around
        player.travel(direction)                                    # go in that


############## CODE END


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
