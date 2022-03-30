import argparse
import pygame
import carla

from .hud import InfoBar
#from .hero import Hero
from .world import World
from .input_control import InputControl
from .hero_with_controller import Hero
from .other_with_controller import Other

from .color import *


def game_loop(args):
    """Initialized, Starts and runs all the needed modules for No Rendering Mode"""
    try:

        # Init Pygame
        pygame.init()
        display = pygame.display.set_mode(
            (args.width, args.height), pygame.HWSURFACE | pygame.DOUBLEBUF
        )

        # Place a title to game window
        pygame.display.set_caption(args.description)

        # Show loading screen
        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        text_surface = font.render("Rendering map...", True, COLOR_WHITE)
        display.blit(
            text_surface,
            text_surface.get_rect(center=(args.width / 2, args.height / 2)),
        )
        pygame.display.flip()

        # Init
        hud = InfoBar(args.width, args.height)
        input_control = InputControl()
        world = World(args)
        

        hero_waypoints = [
            carla.Location(x=-30.6, y=28, z=0.6),
            carla.Location(x=120.6, y=28, z=0.6),
        ]
        
        other1_waypoints = [
            carla.Location(x=-30, y=28, z=0.6),
            carla.Location(x=120, y=28, z=0.6),
        ]
        other2_waypoints = [
            carla.Location(x=-30, y=28, z=0.6),
            carla.Location(x=30, y=28, z=0.6),
            carla.Location(x=35, y=24, z=0.6),
            carla.Location(x=120, y=24, z=0.6),
        ]


        hero = Hero(location = carla.Location(x=-114.6, y=28, z=0.6),
                    rotation = carla.Rotation(yaw=0.0),
                    waypoints = hero_waypoints,
                    target_speed = 12  
                    )
        other1 = Other(location = carla.Location(x=-50.6, y=28, z=0.6),
                        rotation = carla.Rotation(yaw=0.0),
                        waypoints = other1_waypoints,
                        target_speed = 7)
        other2 = Other(location = carla.Location(x=-108.6, y=28, z=0.6),
                        rotation = carla.Rotation(yaw=0.0),
                        waypoints = other2_waypoints,
                        target_speed = 12)




        # For each module, assign other modules that are going to be used inside that module
        hud.start(world)
        input_control.start(hud, world)
        world.start(input_control)

        hero.start(world)
        other1.start(world)
        other2.start(world)
        
        # Game loop
        clock = pygame.time.Clock()
        while True:
            clock.tick_busy_loop(500)

            # Tick all modules
            world.tick(clock)
            hero.tick(clock)
            other1.tick(clock)
            other2.tick(clock)
            hud.tick(clock)
            input_control.tick(clock)

            # Render all modules
            display.fill(COLOR_ALUMINIUM_4)
            world.render(display)
            hud.render(display)
            input_control.render(display)

            pygame.display.flip()

    except KeyboardInterrupt:
        print("\nCancelled by user. Bye!")

    finally:
        if hero is not None:
            hero.destroy()
        if other1 is not None:
            other1.destroy()
        if other2 is not None:
            other2.destroy()    


def main():
    """Parses the arguments received from commandline and runs the game loop"""

    # Define arguments that will be received and parsed
    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        "--host",
        metavar="H",
        default="127.0.0.1",
        help="IP of the host server (default: 127.0.0.1)",
    )
    argparser.add_argument(
        "-p",
        "--port",
        metavar="P",
        default=2000,
        type=int,
        help="TCP port to listen to (default: 2000)",
    )
    argparser.add_argument(
        "--tm-port",
        metavar="P",
        default=8000,
        type=int,
        help="Port to communicate with TM (default: 8000)",
    )
    argparser.add_argument(
        "--timeout",
        metavar="X",
        default=2.0,
        type=float,
        help="Timeout duration (default: 2.0s)",
    )
    argparser.add_argument(
        "--res",
        metavar="WIDTHxHEIGHT",
        default="1280x720",
        help="window resolution (default: 1280x720)",
    )
    argparser.add_argument(
        "--filter",
        metavar="PATTERN",
        default="vehicle.audi.*",
        help='actor filter (default: "vehicle.audi.*")',
    )

    # Parse arguments
    args = argparser.parse_args()
    args.description = "BounCMPE CarlaSim 2D Visualizer"
    args.width, args.height = [int(x) for x in args.res.split("x")]

    # Run game loop
    game_loop(args)
