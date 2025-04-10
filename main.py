#!/usr/bin/env python3

import traceback

import tcod

import color
import exceptions
import setup_game
import input_handlers

def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """If the current event handler has an active Engine then save it"""
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")

def main() -> None:
    screen_width = 80
    screen_height = 50
    
    #tileset = tcod.tileset.load_tilesheet(
    #    "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    #)
    
    tile_pixel_width = 24
    tile_pixel_height = 24
    
    try:
        tileset = tcod.tileset.load_truetype_font(
            "PixelOperator8-Bold.ttf",
            tile_pixel_width,
            tile_pixel_height
        )
    except FileNotFoundError:
        print("Error: the font file was not found")
        raise SystemExit()
    except Exception as e:
        print("Error loading font: {e}")
        raise SystemExit()
    
    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()
    
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)
                
                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception:
                    traceback.print_exc()
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit: # Save and quit
            save_game(handler, "savegame.sav")
            raise
        except BaseException: # Save on any other unexpected exeption
            save_game(handler, "savegame.sav")
            raise
            
                
if __name__ == "__main__":
    main()