from random import randint

import pygame
from data import *
from keyboards import InGameKeyboardManager

from loading import *
from features import *
from mapClasses import *
from keyboards import *
from inventory import *
from menus import *

mm = MenuManager()
gd = GameData()
gc = GameController(gd, mm)
em = EventsManager(gd, gc)
picaso = Picaso(gd, gc)
inv = Inventory(gc, gd)
gc.set_inventory(inv)



def main():
    init_game(gd, gc)
    run_game_loop()

def run_game_loop():
    running = True

    # TODO: deal with this phrase stuff
    # NPC1 = Feature(4, 3, 128, 128, ["assets/NPC.png", "assets/NPC - f2.png", "assets/NPC-blue.png"], "Mary")
    Phrase1 = Phrase("Hello World", True, 100, 300, (255, 255, 255), 20)
    Phrase2 = Phrase("Goodbye World", True, 100, 300, (255, 255, 255), 20)

    # set up the events that allow things to move (add these to the individual classes of each of the dudes)
    printout = pygame.USEREVENT + 3
    pygame.time.set_timer(printout, 500)

    while running:
        print(gd.tiles_img_dict)
        pygame.draw.rect(gc.screen, (0, 0, 0), (0, 0, 1000, 10000))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if gc.input:
                if event.type == pygame.KEYDOWN:
                    gc.current_keyboard_manager.parse_key(event.key)

            if event.type == pygame.KEYUP:
                gc.key_held = False

            # check to see if any events have occurred
            for character in gd.room_list[gc.current_room].character_list:
                    if event.type == gd.character_list[character].initiate:
                        if gd.character_list[character].state == "idle":
                            gd.character_list[character].do_activity()

            #check for a single step in series of walk cycle steps for each character
            for character in gd.room_list[gc.current_room].character_list:
                try:
                    if event.type == gd.character_list[character].action_clock:
                        gd.character_list[character].check_if_walking()
                except AttributeError:
                    pass

            # check for a single step in series of walk cycle steps for Player
            if event.type == gd.player["Player"].step_timer:
                gd.player["Player"].check_if_walking()

        picaso.big_draw()
        pygame.display.update()
        gc.tick()


if __name__ == "__main__":
    main()