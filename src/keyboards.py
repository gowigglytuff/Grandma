from abc import ABC, abstractmethod

import pygame

#TODO add other keyboards
class KeyboardManager(ABC):

    @property
    @abstractmethod
    def ID(self):
        pass

    def parse_key(self, key_pressed):
        self.key_pushed()

        if key_pressed == pygame.K_RIGHT:
            self.key_right()

        if key_pressed == pygame.K_LEFT:
            self.key_left()

        if key_pressed == pygame.K_DOWN:
            self.key_down()

        if key_pressed == pygame.K_UP:
            self.key_up()

        if key_pressed == pygame.K_RETURN:
            self.key_return()

        if key_pressed == pygame.K_SPACE:
            self.key_space()

        if key_pressed == pygame.K_LCTRL:
            self.key_control()

        if key_pressed == pygame.K_LSHIFT:
            self.key_shift()

        if key_pressed == pygame.K_CAPSLOCK:
            self.key_caps()

    def key_pushed(self):
        pass

    @abstractmethod
    def key_right(self):
        pass

    @abstractmethod
    def key_left(self):
        pass

    @abstractmethod
    def key_down(self):
        pass

    @abstractmethod
    def key_up(self):
        pass

    @abstractmethod
    def key_return(self):
        pass


    @abstractmethod
    def key_space(self):
        pass

    @abstractmethod
    def key_control(self):
        pass

    @abstractmethod
    def key_shift(self):
        pass


class InGameKeyboardManager(KeyboardManager):
    ID = "IG_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_pushed(self):
        self.GameController.key_held = True

    def key_right(self):
        self.GameData.player["Player"].try_walk_right()

    def key_left(self):
        self.GameData.player["Player"].try_walk_left()

    def key_up(self):
        self.GameData.player["Player"].try_walk_back()

    def key_down(self):
        self.GameData.player["Player"].try_walk_front()

    def key_return(self):
        # interacts with the feature that is in the tile that the player is facing
        self.GameData.player["Player"].interact_with()

    def key_space(self):
        self.GameController.inventory.change_bag_slot()

    def key_control(self):
        self.GameController.set_keyboard_manager(InStartMenuKeyboardManager.ID)
        #         # self.GameController.set_menu("start_menu")
        self.GameController.MenuManager.start_menu = True


    def key_shift(self):
        # self.GameController.set_keyboard_manager(InMenuKeyboardManager.ID)
        # self.GameController.set_menu("testing_menu")
        pass

    def key_caps(self):
        pass


class InMenuKeyboardManager(KeyboardManager):
    ID = "IM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        pass

    def key_left(self):
        pass

    def key_up(self):

        menu = self.GameData.menu_list["testing_menu"].menu_item_list
        menu.append(menu.pop(menu.index(menu[0])))

    def key_down(self):
        menu = self.GameData.menu_list["testing_menu"].menu_item_list
        menu.insert(0, menu.pop(-1))

    def key_return(self):
        self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
        self.GameController.set_menu(None)

    def key_space(self):
        pass

    def key_control(self):
        pass

    def key_shift(self):
        pass

    def key_caps(self):
        pass


class InInventoryMenuKeyboardManager(KeyboardManager):
    ID = "IIM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        self.GameController.MenuManager.inventory_menu = False
        self.GameController.MenuManager.key_inventory_menu = True
        self.GameController.set_keyboard_manager(InKeyInventoryMenuKeyboardManager.ID)

    def key_left(self):
        self.GameController.MenuManager.inventory_menu = False
        self.GameController.MenuManager.key_inventory_menu = True
        self.GameController.set_keyboard_manager(InKeyInventoryMenuKeyboardManager.ID)

    def key_up(self):
        self.GameData.menu_list["inventory_menu"].cursor_up()

    def key_down(self):
        self.GameData.menu_list["inventory_menu"].cursor_down()

    def key_return(self):
        menu_selection = self.GameData.menu_list["inventory_menu"].get_current_menu_item()
        self.GameController.inventory.select_item(menu_selection)
        self.GameController.set_keyboard_manager(InUseInventoryMenuKeyboardManager.ID)
        self.GameController.MenuManager.use_menu = True

    def key_space(self):
        pass

    def key_control(self):
        pass

    def key_shift(self):
        pass

    def key_caps(self):
        pass


class InKeyInventoryMenuKeyboardManager(KeyboardManager):
    ID = "IKM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        self.GameController.MenuManager.key_inventory_menu = False
        self.GameController.MenuManager.inventory_menu = True
        self.GameController.set_keyboard_manager(InInventoryMenuKeyboardManager.ID)

    def key_left(self):
        self.GameController.MenuManager.key_inventory_menu = False
        self.GameController.MenuManager.inventory_menu = True
        self.GameController.set_keyboard_manager(InInventoryMenuKeyboardManager.ID)

    def key_up(self):
        self.GameData.menu_list["key_inventory_menu"].cursor_up()

    def key_down(self):
        self.GameData.menu_list["key_inventory_menu"].cursor_down()

    def key_return(self):
        menu_selection = self.GameData.menu_list["key_inventory_menu"].get_current_menu_item()
        self.GameController.inventory.select_item(menu_selection)
        self.GameController.set_keyboard_manager(InUseKeyInventoryMenuKeyboardManager.ID)
        self.GameController.MenuManager.use_menu = True

    def key_space(self):
        pass

    def key_control(self):
        pass

    def key_shift(self):
        pass

    def key_caps(self):
        pass


class InStartMenuKeyboardManager(KeyboardManager):
    ID = "ISM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        pass

    def key_left(self):
        pass

    def key_up(self):
        self.GameData.menu_list["start_menu"].cursor_up()

    def key_down(self):
        self.GameData.menu_list["start_menu"].cursor_down()

    def key_return(self):
        menu_selection = self.GameData.menu_list["start_menu"].get_current_menu_item()
        if menu_selection == "Bag":
            print("You looked in your bag!")

            # self.GameController.set_menu(None)
            self.GameController.MenuManager.start_menu = False
            self.GameController.MenuManager.inventory_menu = True
            self.GameController.set_keyboard_manager(InInventoryMenuKeyboardManager.ID)
            self.GameData.menu_list["start_menu"].reset_cursor()

        elif menu_selection == "Key Items":
            print("You looked in your bag!")

            # self.GameController.set_menu(None)
            self.GameController.MenuManager.start_menu = False
            self.GameController.MenuManager.key_inventory_menu = True
            self.GameController.set_keyboard_manager(InKeyInventoryMenuKeyboardManager.ID)
            self.GameData.menu_list["start_menu"].reset_cursor()

        elif menu_selection == "Profile":
            self.GameController.add_current_overlay("ID_card")
            self.GameController.MenuManager.start_menu = False
            self.GameController.set_keyboard_manager(InProfileKeyboardManager.ID)
            self.GameData.menu_list["start_menu"].reset_cursor()


        else:
            print("You exited the menu")
            self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
            # self.GameController.set_menu(None)
            self.GameController.MenuManager.start_menu = False
            self.GameData.menu_list["start_menu"].reset_cursor()


    def key_space(self):
        pass

    def key_control(self):
        self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
        # self.GameController.set_menu(None)
        self.GameController.MenuManager.start_menu = False

    def key_shift(self):
        pass

    def key_caps(self):
        pass


class InUseInventoryMenuKeyboardManager(KeyboardManager):
    ID = "IUM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        pass

    def key_left(self):
        pass

    def key_up(self):
        self.GameData.menu_list["use_menu"].cursor_up()

    def key_down(self):
        self.GameData.menu_list["use_menu"].cursor_down()

    def key_return(self):
        menu_selection = self.GameData.menu_list["use_menu"].get_current_menu_item()

        if menu_selection == "Use":
            self.GameData.item_list[self.GameController.inventory.selected_item].use_item()

            # self.GameController.set_menu(None)
            self.GameController.inventory.select_item(None)
            self.GameController.MenuManager.use_menu = False
            self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
            self.GameController.MenuManager.inventory_menu = False

        elif menu_selection == "Toss":
            print("You looked in your bag!")

            # self.GameController.set_menu(None)
            self.GameController.MenuManager.use_menu = False
            self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
            self.GameController.MenuManager.inventory_menu = False
            self.GameController.MenuManager.key_inventory_menu = False

        elif menu_selection == "Exit":

            print("You looked in your bag!")
            # self.GameController.set_menu(None)
            self.GameController.MenuManager.use_menu = False
            self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
            self.GameController.MenuManager.inventory_menu = False
            self.GameController.MenuManager.key_inventory_menu = False

    def key_space(self):
        pass

    def key_control(self):
        self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
        # self.GameController.set_menu(None)
        self.GameController.MenuManager.start_menu = False

    def key_shift(self):
        pass

    def key_caps(self):
        pass

class InUseKeyInventoryMenuKeyboardManager(KeyboardManager):
    ID = "IUKM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        pass

    def key_left(self):
        pass

    def key_up(self):
        self.GameData.menu_list["use_menu"].cursor_up()

    def key_down(self):
        self.GameData.menu_list["use_menu"].cursor_down()

    def key_return(self):
        menu_selection = self.GameData.menu_list["use_menu"].get_current_menu_item()

        if menu_selection == "Use":
            self.GameData.key_item_list[self.GameController.inventory.selected_item].use_item()

            # self.GameController.set_menu(None)
            self.GameController.inventory.select_item(None)
            self.GameController.MenuManager.use_menu = False
            self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
            self.GameController.MenuManager.key_inventory_menu = False

        elif menu_selection == "Toss":
            print("You looked in your bag!")

            # self.GameController.set_menu(None)
            self.GameController.MenuManager.use_menu = False
            self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
            self.GameController.MenuManager.inventory_menu = False
            self.GameController.MenuManager.key_inventory_menu = False

        elif menu_selection == "Exit":

            print("You looked in your bag!")
            # self.GameController.set_menu(None)
            self.GameController.MenuManager.use_menu = False
            self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
            self.GameController.MenuManager.inventory_menu = False
            self.GameController.MenuManager.key_inventory_menu = False

    def key_space(self):
        pass

    def key_control(self):
        self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
        # self.GameController.set_menu(None)
        self.GameController.MenuManager.start_menu = False

    def key_shift(self):
        pass

    def key_caps(self):
        pass


class InConversationKeyboardManager(KeyboardManager):
    ID = "IT_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        pass

    def key_left(self):
        pass

    def key_up(self):
        pass

    def key_down(self):
        pass

    def key_return(self):
        if self.GameData.character_list[self.GameData.player["Player"].get_facing_tile().object_filling].current_phrase != None:
            self.GameData.character_list[self.GameData.player["Player"].get_facing_tile().object_filling].set_speaking_queue()
        else:
            self.GameData.character_list[
                self.GameData.player["Player"].get_facing_tile().object_filling].clear_speaking_queue()
            self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
            self.GameData.character_list[self.GameController.current_speaker].set_state("idle")
            self.GameController.set_text_box(None)
            self.GameController.set_speaker(None)


    def key_space(self):
        pass

    def key_control(self):
        pass

    def key_shift(self):
        pass

    def key_caps(self):
        pass


class InTalkingMenuKeyboardManager(KeyboardManager):
    ID = "ITKM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        pass

    def key_left(self):
        pass

    def key_up(self):
        self.GameData.menu_list["character_interact_menu"].cursor_up()

    def key_down(self):
        self.GameData.menu_list["character_interact_menu"].cursor_down()

    def key_return(self):
        #TODO: Fix this to use characters name instead of facing tile
        menu_selection = self.GameData.menu_list["character_interact_menu"].get_current_menu_item()
        if menu_selection == self.GameData.menu_list["character_interact_menu"].menu_item_list[0]:
            self.GameController.set_speaker(self.GameData.player["Player"].get_facing_tile().object_filling)
            self.GameData.character_list[self.GameData.player["Player"].get_facing_tile().object_filling].set_state("talking")
            self.GameData.character_list[self.GameData.player["Player"].get_facing_tile().object_filling].set_current_phrase()
            self.GameData.character_list[self.GameData.player["Player"].get_facing_tile().object_filling].set_speaking_queue()
            self.GameController.set_keyboard_manager(InConversationKeyboardManager.ID)
            #self.GameController.set_menu(None)
            self.GameData.menu_list["character_interact_menu"].set_talking_to(None)
            self.GameController.MenuManager.character_interact_menu = False


    def key_space(self):
        pass

    def key_control(self):
        self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
        self.GameController.set_menu(None)

    def key_shift(self):
        pass

class InProfileKeyboardManager(KeyboardManager):
    ID = "IPM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        pass

    def key_left(self):
        pass

    def key_up(self):
        pass

    def key_down(self):
        pass

    def key_return(self):
        self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
        self.GameController.remove_current_overlay("ID_card")

    def key_space(self):
        pass

    def key_control(self):
        self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)

    def key_shift(self):
        pass

    def key_caps(self):
        pass