import pygame

class Overlay(object):
    def __init__(self, GameController, GameData, name, x, y, image):
        self.GameController = GameController
        self. GameData = GameData
        self.screen = self.GameController.screen
        self.x = x
        self.y = y
        self.name = name
        self.image = image.get_image(0, 0)

    def display_overlay(self):
        self.screen.blit(self.image, (self.x, self.y))

class ProfileCard(Overlay):
    def __init__(self, GameController, GameData, name, x, y, image):
        super().__init__(GameController, GameData, name, x, y, image)

    def display_overlay(self):
        self.screen.blit(self.image, (self.x, self.y))
        self.screen.blit(self.GameData.player["Player"].spritesheet.get_image(0, 0),( self.x +57, self.y +50))

        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render("Name: Jayden", 1, (0, 0, 0))
        self.GameController.screen.blit(item, (self.x +125, self.y + 40))

        item2 = my_font.render("Reputation: ", 1, (0, 0, 0))
        self.GameController.screen.blit(item2, (self.x + 125, self.y + 60))

class TextBox(Overlay):
    def __init__(self, GameController, GameData, name, x, y, image):
        super().__init__(GameController, GameData, name, x, y, image)

    def display_phrase(self, character):
    # prints the speakers name
        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render(self.GameData.character_list[character].name + ":", 1, (0, 0, 0))
        self.GameController.screen.blit(item, (
        self.GameData.overlay_list["text_box"].x + 150, self.GameData.overlay_list["text_box"].y + 20))

        # prints phrases to be spoke
        text_line = 0
        for line in self.GameData.character_list[character].speaking_queue:
            my_font = pygame.font.Font(self.GameController.font, 10)
            item = my_font.render(line, 1, (0, 0, 0))
            self.GameController.screen.blit(item, (self.GameData.overlay_list["text_box"].x + 150,
                                                   self.GameData.overlay_list["text_box"].y + 50 + 25 * text_line))
            text_line += 1

class MenuManager(object):
    def __init__(self):
        self.character_interact_menu = False
        self.start_menu = False
        self.inventory_menu = False
        self.key_inventory_menu = False
        self.use_menu = False

class Menu(object):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay, offset_x=30, offset_y=20):
        self.GameController = GameController
        self.GameData = GameData
        self.screen = self.GameController.screen
        self.overlay = overlay
        self.x = self.GameData.overlay_list[self.overlay].x + offset_x
        self.y = self.GameData.overlay_list[self.overlay].y + offset_y
        self.name = name
        self.menu_item_list = menu_item_list
        self.menu_spread = 25
        self.menu_go = menu_go
        self.cursor_at = 0


    @property
    def size(self):
        return len(self.menu_item_list)

    def reset_cursor(self):
        self.cursor_at = 0

    def display_cursor(self):
        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render("-", 1, (0, 0, 0))
        self.screen.blit(item, (self.x - 15, (self.y+2) + (self.cursor_at * self.menu_spread)))

    def display_menu(self):
        self.GameData.overlay_list[self.overlay].display_overlay()
        for option in range(self.size):
            my_font = pygame.font.Font(self.GameController.font, 10)
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))
        self.display_cursor()

    def cursor_down(self):
        if self.cursor_at == len(self.menu_item_list) -1:
            self.cursor_at = 0
        else:
            self.cursor_at += 1

    def cursor_up(self):
        if self.cursor_at == 0:
            self.cursor_at = len(self.menu_item_list) -1
        else:
            self.cursor_at -= 1

    #TODO: Make it so you can change which bag slot you're in by pressing left and right
    # def cursor_left(self):
    #     self.GameController.inventory.bag_slots

    def get_current_menu_item(self):
        menu_selection = self.menu_item_list[self.cursor_at]
        return menu_selection

class TalkingMenu(Menu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay, offset_x=150, offset_y = 50)
        self.talking_to = None
        self.menu_item_list.append("Exit")

    def set_talking_to(self, talking_to):
        self.talking_to = talking_to

    def display_menu(self):
        self.GameData.overlay_list[self.overlay].display_overlay()
        for option in range(self.size):
            my_font = pygame.font.Font(self.GameController.font, 10)
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + (option*self.menu_spread)))
        self.display_cursor()

        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render(self.GameData.character_list[self.talking_to].name + ":", 1, (0, 0, 0))
        self.GameController.screen.blit(item, (
            self.GameData.overlay_list["text_box"].x + 150, self.GameData.overlay_list["text_box"].y + 20))

class StartMenu(Menu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay)
        self.menu_item_list.append("Exit")

class InventoryMenu(Menu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay)
        self.y_spacing = 20

    def display_cursor(self):
        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render("-", 1, (0, 0, 0))
        self.screen.blit(item, (self.x - 15, (self.y+2 + self.y_spacing) + (self.cursor_at * self.menu_spread)))

    def display_menu(self):
        self.GameData.overlay_list[self.overlay].display_overlay()

        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render("<    ITEMS    >", 1, (0, 0, 0))
        self.screen.blit(item, (self.x, self.y))

        for option in range(self.size):
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + self.y_spacing + (option * self.menu_spread)))

            spacing = 0
            if len(str(self.GameData.item_list[self.menu_item_list[option]].quantity)) == 3:
                spacing = 110
            elif len(str(self.GameData.item_list[self.menu_item_list[option]].quantity)) == 2:
                spacing = 120
            else:
                spacing = 130

            item = my_font.render("x" + str(self.GameData.item_list[self.menu_item_list[option]].quantity), 1, (0, 0, 0))
            self.screen.blit(item, (self.x + spacing, self.y + self.y_spacing + (option * self.menu_spread)))
        self.display_cursor()

class KeyInventoryMenu(Menu):
    def __init__(self, GameController, GameData, name, menu_item_list, menu_go, overlay):
        super().__init__(GameController, GameData, name, menu_item_list, menu_go, overlay)
        self.y_spacing = 20

    def display_cursor(self):
        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render("-", 1, (0, 0, 0))
        self.screen.blit(item, (self.x - 15, (self.y+2 + self.y_spacing) + (self.cursor_at * self.menu_spread)))

    def display_menu(self):
        self.GameData.overlay_list[self.overlay].display_overlay()

        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render("<  KEY ITEMS  >", 1, (0, 0, 0))
        self.screen.blit(item, (self.x, self.y))

        for option in range(self.size):
            item = my_font.render(self.menu_item_list[option], 1, (0, 0, 0))
            self.screen.blit(item, (self.x, self.y + self.y_spacing + (option * self.menu_spread)))

        self.display_cursor()