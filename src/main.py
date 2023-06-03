import argparse
import json
import logging
import os
import sys

import pymunk

from config import config
from game import Game
from map import Map
from replay import ReplayManager


def run(replay: ReplayManager, map_name, use_pygame=False):

    m = Map(map_name=map_name)
    running = True
    space = pymunk.Space()
    game = Game(space, m, replay)

    with open(map_name) as mapFile:
        replay.post_custom_replay_line({"map": mapFile.read().splitlines()})
    replay.post_custom_replay_line({"client_info": game.comms.client_info})

    if use_pygame:
        import pygame
        from pymunk import pygame_util

        pygame_util.positive_y_is_up = True
        pygame.init()
        display = pygame.display.set_mode(
            (
                (m.map_width + 1) * config.GRID_SCALING,
                (m.map_height + 1) * config.GRID_SCALING,
            )
        )
        clock = pygame.time.Clock()
        draw_options = pymunk.pygame_util.DrawOptions(display)  # type: ignore

    while running:
        for i in range(config.SIMULATION.PHYSICS_ITERATIONS_PER_COMMUNICATION):
            if use_pygame:
                # Visual mainloop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break

                # Reset screen and draw all physics objects
                display.fill(pygame.Color("white"))
                space.debug_draw(draw_options)

            for _ in range(config.SIMULATION.PYMUNK_TIMESTEP_ITERATIONS):
                # Update physics and do game logic.
                space.step(config.SIMULATION.PHYSICS_TIMESTEP)
                if game.tick():  # game is terminal
                    running = False
                    break
            if not running:
                break

            replay.set_game_info(space)
            replay.post_replay_line(
                include_events=i
                == config.SIMULATION.PHYSICS_ITERATIONS_PER_COMMUNICATION - 1
            )

            if use_pygame:
                pygame.display.flip()
                clock.tick(config.SIMULATION.PYGAME_FPS)

        if running:
            replay.set_game_info(space)
            comms_line = replay.get_comms_line()
            game.comms.post_message(message=comms_line)
            game.handle_client_response()
        else:
            results = game.results()
            replay.post_custom_replay_line(results)  # post results in replay file
            with open("replay/results.json", "w") as file:
                file.write(json.dumps(results, separators=(",", ":")))

    if use_pygame:
        pygame.quit()


def game_started():
    import os.path

    return os.path.isfile("/codequest/GAME_STARTED")


if __name__ == "__main__":
    logging.basicConfig(
        filename="replay/server.log", encoding="utf-8", level=logging.INFO
    )
    logging.info(sys.argv)

    while not sys.argv[-1].strip():
        del sys.argv[-1]

    parser = argparse.ArgumentParser(
        prog="GameServer", description="Game server for codequest-23 competition"
    )

    parser.add_argument("-m", "--map", default="nuketown.map")
    args = parser.parse_args()

    replay = ReplayManager(config.REPLAY.PATH)

    try:
        run(
            replay,
            map_name=config.MAP.DIR + args.map or config.MAP.NUKETOWN,
            use_pygame=str(os.environ.get("USE_PYGAME", 1)) == "1",
        )
    except Exception as e:
        replay.close()
        raise e
    finally:
        replay.close()
