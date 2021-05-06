import pygame, csv, os


class Room(object):

    def __init__(self, name, left_edge_x, top_edge_y, room_width, room_height, total_plots_x, total_plots_y, plot_size_x, plot_size_y, GameController, GameData, map_style="image"):
        self.GameController = GameController
        self.GameData = GameData

        self.name = name
        self.left_edge_x = left_edge_x
        self.right_edge_x = left_edge_x + room_width - 1
        self.top_edge_y = top_edge_y
        self.bottom_edge_y = top_edge_y + room_height - 1
        self.room_width = room_width
        self.room_height = room_height
        self.map_style = map_style

        self.plot_list = {}
        self.total_plots_x = total_plots_x
        self.total_plots_y = total_plots_y
        self.plot_size_x = plot_size_x
        self.plot_size_y = plot_size_y
        self.active_plots = []

        self.tiles_array = []
        self.active_tiles = []

        self.door_list = {}
        self.character_list = []
        self.decoration_list = []
        self.prop_list = []


    def generate_room_grid(self):
        """
        adds an array to tiles_array which is a grid for the current room
        :return: null
        """
        for section in range(self.room_width + 3):
            section_name = []
            self.tiles_array.append(section_name)

        for letter in range(self.room_width + 2):
            for number in range(self.room_height + 3):
                spot_name = Tile(letter, number, False, "None", "None")
                self.tiles_array[letter].append(spot_name)

    def add_room_plot(self, plot_name, plot_object):
        self.plot_list[plot_name] = plot_object

    def add_room_character(self, character_name):
        self.character_list.append(character_name)

    def add_room_prop(self, prop_name):
        self.prop_list.append(prop_name)

    def add_room_decoration(self, decoration_name):
        self.decoration_list.append(decoration_name)

    def add_room_door(self, door_name, door_object):
        self.door_list[door_name] = door_object

    def activate_plot(self, plot_name):
        self.active_plots.append(plot_name)

    def draw_bg(self, screen):
        for plot in self.active_plots:
            self_x = (((((self.plot_list[plot].plot_x)-1)*self.plot_size_x + self.GameController.camera[0])+1) * self.GameData.square_size[0]) + self.GameData.base_locator_x
            self_y = (((((self.plot_list[plot].plot_y)-1)*self.plot_size_y + self.GameController.camera[1])+1) * self.GameData.square_size[1]) + self.GameData.base_locator_y
            screen.blit(self.plot_list[plot].plot_img, (self_x, self_y))

class Plot(object):
    '''
    each room will be made up of a specified number of plots
    '''
    def __init__(self, room, plot_x, plot_y, plot_img, GameController, GameData, csv_file):
        self.GameController = GameController
        self.GameData = GameData

        self.room = room
        self.plot_x = plot_x
        self.plot_y = plot_y
        self.name = self.room + "_" + str(plot_x) + "_"+ str(plot_y)
        self.plot_img = plot_img
        self.csv_file = csv_file
        self.prop_list = []
        self.character_list = []
        self.decoration_list = []


class Tile(object):

    DOOR = "Door"
    NPC = "NPC"
    PIXIE = "Pixie"
    PLAYER = "Player"
    NONE = "None"
    PROP = "Prop"
    OBSTACLE = "Obstacle"
    TILE_TYPE_LIST = [DOOR, NPC, PLAYER, PIXIE, PROP, NONE, OBSTACLE]

    def __init__(self, x, y, full, object_filling, filling_type, item=None):
        assert filling_type in self.TILE_TYPE_LIST
        self.x = x
        self.y = y
        self.full = full
        self.object_filling = object_filling
        self.filling_type = filling_type
        self.item = item
        self.name = "tile" + str(x) + "_" + str(y)
        self.elevation = 1


class Door(object):
    def __init__(self, room_from, room_to, x, y, exit_x, exit_y, name):
        self.room_from = room_from
        self.room_to = room_to
        self.x = x
        self.y = y
        self.exit_x = exit_x
        self.exit_y = exit_y
        self.name = name

class BG(object):
    def __init__(self, x, y, name, img_file_name_list, GameController, GameData):
        self.x = x
        self.y = y
        self.img_file_name_list = img_file_name_list
        self.img_list = [file_name for file_name in
                        img_file_name_list]

        self.cur_img = 0
        self.img = self.img_list[self.cur_img]
        self.name = name
        self.GameController = GameController
        self.GameData = GameData

    def draw(self, screen):
        screen.blit(self.img,
                    (((self.x + self.GameController.camera[0]) * self.GameData.square_size[0]) + self.GameData.base_locator_x,
                    ((self.y + self.GameController.camera[1]) * self.GameData.square_size[1]) + self.GameData.base_locator_y))


class Position_Manager(object):
    def __init__(self, name, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData
        self.name = name

    def fill_tiles(self, fillable_room):
        for tile_list in self.GameData.room_list[fillable_room].tiles_array:
            for tile in tile_list:
                drawable_list = self.GameController.get_current_drawables(fillable_room)
                for drawable in drawable_list:
                    if drawable.feature_type == "Prop" and drawable.x == tile.x and drawable.y == tile.y:
                        for size_x in range(drawable.size_x):
                            for size_y in range(drawable.size_y):
                                    self.GameData.room_list[fillable_room].tiles_array[drawable.x + size_x][drawable.y + size_y].object_filling = drawable.name
                                    self.GameData.room_list[fillable_room].tiles_array[drawable.x + size_x][drawable.y + size_y].filling_type = drawable.feature_type
                                    self.GameData.room_list[fillable_room].tiles_array[drawable.x + size_x][drawable.y + size_y].full = True

                    elif drawable.feature_type != "Prop" and drawable.x == tile.x and drawable.y == tile.y:
                        tile.object_filling = drawable.name
                        tile.filling_type = drawable.feature_type
                        tile.full = True

    def fill_obstacles(self, filename, fillable_room):
        for plot in self.GameData.room_list[fillable_room].active_plots:
            current_plot = self.GameData.room_list[fillable_room].plot_list[plot]
            map = self.read_csv(self.GameData.room_list[fillable_room].plot_list[plot].csv_file)
            x, y = (current_plot.plot_x-1) * self.GameData.room_list[fillable_room].plot_size_x, (current_plot.plot_y-1) * self.GameData.room_list[fillable_room].plot_size_y
            for row in map:
                x = (current_plot.plot_x-1) * self.GameData.room_list[fillable_room].plot_size_x
                for tile in row:
                    if tile == "0":
                        pass
                    elif tile == "1":
                        tile = self.GameData.room_list[fillable_room].tiles_array[x+1][y+1]
                        tile.object_filling = "Obstacle"
                        tile.filling_type = "Obstacle"
                        tile.full = True
                    x += 1
                y += 1

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def fill_doors(self, fillable_room):
        for tile_list in self.GameData.room_list[fillable_room].tiles_array:
            for tile in tile_list:
                for door in self.GameData.room_list[fillable_room].door_list:
                    if self.GameData.room_list[fillable_room].door_list[door].x == tile.x and self.GameData.room_list[fillable_room].door_list[door].y == tile.y:
                        tile.object_filling = self.GameData.room_list[fillable_room].door_list[door].name
                        tile.filling_type = "Door"
                        tile.full = True

    def through_door(self, door):
        self.empty_tile(self.GameData.player["Player"])
        x_change = self.GameData.player["Player"].x - door.exit_x
        y_change = self.GameData.player["Player"].y - door.exit_y
        self.GameData.player["Player"].x = door.exit_x
        self.GameData.player["Player"].y = door.exit_y
        self.GameData.player["Player"].turn_front()
        self.GameController.camera[0] += x_change
        self.GameController.camera[1] += y_change
        self.GameController.set_room(door.room_to)
        self.empty_tiles(door.room_to)
        #TODO: Make all maps in CSV Style?
        if self.GameData.room_list[door.room_to].map_style == "csv":
            for plot in self.GameData.room_list[door.room_to].plot_list:
                self.fill_obstacles(self.GameData.room_list[door.room_to].plot_list[plot].csv_file, door.room_to)
        self.fill_tiles(door.room_to)
        self.fill_doors(door.room_to)
        self.fill_tile(self.GameData.player["Player"])


    def empty_tiles(self, fillable_room):
        #FIXME: dum dum
        for tile_list in self.GameData.room_list[fillable_room].tiles_array:
            for tile in tile_list:
                tile.object_filling = "None"
                tile.filling_type = "None"
                tile.full = False

    def can_move(self, mover):
        move = False
        facing_tile = mover.get_facing_tile()
        if mover.facing == "left":
            if mover.x <= self.GameData.room_list[self.GameController.current_room].left_edge_x:
                move = False
            else:
                if not facing_tile.full:
                    move = True
                else:
                    move = False
        elif mover.facing == "right":
            if mover.x >= self.GameData.room_list[self.GameController.current_room].right_edge_x:
                move = False
            else:
                if not facing_tile.full:
                    move = True
                else:
                    move = False
        elif mover.facing == "front":
            if mover.y >= self.GameData.room_list[self.GameController.current_room].bottom_edge_y:
                move = False
            else:
                if not facing_tile.full:
                    move = True
                else:
                    move = False
        if mover.facing == "back":
            if mover.y <= self.GameData.room_list[self.GameController.current_room].top_edge_y:
                move = False
            else:
                if not facing_tile.full:
                    move = True
                else:
                    move = False

        return move

    def check_door(self, mover):
        is_door = False
        facing_tile = mover.get_facing_tile()
        if facing_tile.filling_type == "Door":
            is_door = True
        else:
            is_door = False
        return is_door

    def empty_tile(self, mover):
        self.GameData.room_list[self.GameController.current_room].tiles_array[mover.x][mover.y].full = False
        self.GameData.room_list[self.GameController.current_room].tiles_array[mover.x][mover.y].object_filling = "None"
        self.GameData.room_list[self.GameController.current_room].tiles_array[mover.x][mover.y].filling_type = "None"
    def fill_tile(self, mover):
        self.GameData.room_list[self.GameController.current_room].tiles_array[mover.x][mover.y].full = True
        self.GameData.room_list[self.GameController.current_room].tiles_array[mover.x][mover.y].object_filling = mover.name
        self.GameData.room_list[self.GameController.current_room].tiles_array[mover.x][mover.y].filling_type = mover.feature_type



