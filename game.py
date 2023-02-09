from world import World
import math
import numpy as np
from enum import Enum
import pygame

from robots.bot_list import BotList

# The glue between the World and Pygame
# Includes rendering
class Game:

    class State(Enum):
        PLAY = 1
        PAUSE = 2
        STEP = 3
        FAST = 4
        RESET = 5

    class Button:
        def __init__(self, position, size, text, callback):
            self.position = position
            self.size = size
            self.text = text
            self.callback = callback
        
        def is_at_position(self, position):
            return position[0] >= self.position[0] and position[0] <= self.position[0] + self.size[0] and \
                    position[1] >= self.position[1] and position[1] <= self.position[1] + self.size[1]

    BUTTON = (119,136,153)
    WHITE = (255, 255, 255)
    GREY = (128, 128, 128)
    BLACK = (0, 0, 0)

    FPS_NORMAL = 10
    FPS_FAST = 50

    # 20 (actually 18, because black/white was removed) colours 
    # From: https://sashamaps.net/docs/resources/20-colors/
    COLOURS = [
        (230, 25, 75),
        (60, 180, 75),
        (255, 225, 25),
        (0, 130, 200),
        (245, 130, 48),
        (145, 30, 180),
        (70, 240, 240),
        (240, 50, 230),
        (210, 245, 60),
        (250, 190, 212),
        (0, 128, 128),
        (220, 190, 255),
        (170, 110, 40),
        (255, 250, 200),
        (128, 0, 0),
        (170, 255, 195),
        (128, 128, 0),
        (255, 215, 180),
        (0, 0, 128),
        (128, 128, 128),
    ]

    def button_handler(self, cmd):
        if cmd == self.State.PLAY:
            self.state = self.State.PLAY
            self.FPS = self.FPS_NORMAL
        elif cmd == self.State.PAUSE:
            self.state = self.State.PAUSE
        elif cmd == self.State.STEP:
            self.state = self.State.STEP
        elif cmd == self.State.FAST:
            self.state = self.State.PLAY
            self.FPS = self.FPS_FAST
        elif cmd == "reset":
            self.setup()
            self.state = self.State.STEP
        if cmd == "id":
            self.draw_bot_ids = not self.draw_bot_ids

    def __init__(self, window):
        self.state = self.State.PAUSE
        self.FPS = self.FPS_NORMAL
        self.number_of_rounds = 1000

        self.world = World()
        self.add_bots()
        self.draw_bot_ids = False

        self.window = window
        
        # The canvas is where all the colours will be drawn
        self.canvas = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)
        self.canvas.set_alpha(100)

        # The scoreboard is where all the scores will be printed
        self.scoreboard = pygame.Surface(self.window.get_size())
        self.font = pygame.font.SysFont(None, 24)

        # Keep track of buttons
        self.buttons = []
        size = (50, 30)
        border = 5
        x = self.window.get_height() + border
        y = self.window.get_height() - border - size[1]
        self.buttons += [self.Button((x, y), size, "Play", lambda: self.button_handler(self.State.PLAY))]
        x += size[0] + 2 * border
        self.buttons += [self.Button((x, y), size, "Stop", lambda: self.button_handler(self.State.PAUSE))]
        x += size[0] + 2 * border
        self.buttons += [self.Button((x, y), size, "Step", lambda: self.button_handler(self.State.STEP))]
        x += size[0] + 2 * border
        self.buttons += [self.Button((x, y), size, "Fast", lambda: self.button_handler(self.State.FAST))]
        x += size[0] + 2 * border
        self.buttons += [self.Button((x, y), size, "Reset", lambda: self.button_handler("reset"))]
        x += size[0] + 2 * border
        self.buttons += [self.Button((x, y), size, "Id#", lambda: self.button_handler("id"))]

    def add_bots(self):
        for bot in BotList:
            self.world.add_bot(bot)

    def setup(self):
        self.done = False
        self.world.setup(self.number_of_rounds)
        self.cell_w = math.floor(min(self.canvas.get_size()) / self.world.grid_length)
        self.canvas_font = pygame.font.SysFont(None, math.ceil(self.cell_w * 0.8))

    def process(self):
        if self.state != self.State.PAUSE:
            if self.done:
                self.setup()
            if self.step():
                # Game is done.
                self.done = True
                self.state = self.State.PAUSE
            if self.state == self.State.STEP:
                self.state = self.State.PAUSE
        
        self.render()
        pygame.display.update()

        if self.FPS == self.FPS_FAST:
            return 0
        # This is not ideal because it will wait the same amount regardless
        # if this process was quick or took a long time. We can't simply time
        # it because this is called asynchronously when running in browser.
        # Deemed good enough for now, the tournament won't be run with GUI anyway.
        return 1 / self.FPS # Amount of time that should be waited before the next process

    def step(self) -> bool:
        # return true if game is done
        return self.world.step()

    def colour_from_id(self, id):
        if id == 0: return self.WHITE
        return self.COLOURS[self.world.colour_map[id] % len(self.COLOURS)]

    def render(self):
        self.window.fill(self.WHITE)
        grid = self.world.grid
        w = self.cell_w

        # Draw the colours
        for ix, iy  in np.ndindex(grid.shape):
            colour_id = grid[iy, ix]
            colour = self.colour_from_id(colour_id)
            position = (ix * w, 
                        # Invert the y, so that (0,0) is actually lower left
                        self.window.get_height() - (iy + 1) * w
                        )
            pygame.draw.rect(self.canvas, colour, (*position, w, w))

            if self.draw_bot_ids:
                text_to_render = f"{colour_id}"
                text = self.canvas_font.render(text_to_render, True, self.BLACK + (50,))
                text_size = self.canvas_font.size(text_to_render)
                self.canvas.blit(text, (position[0] + w/2 - text_size[0]/2, position[1] + w/2 - text_size[1]/2))
        self.window.blit(self.canvas, (0, 0)) # We blit also so that we can set a custom alpha

        # Draw the bots
        for bot in self.world.bots:
            position = ((bot.position[0]+0.5) * w, 
                        # Invert the y, so that (0,0) is actually lower left
                        self.window.get_height() - ((bot.position[1]+0.5) * w))
            pygame.draw.circle(self.window, self.colour_from_id(bot.id), position, w * 0.4, math.ceil(w/3))
            pygame.draw.circle(self.window, (0, 0, 0), position, w * 0.4, math.ceil(w/10))
            
        # Draw the score board
        self.scoreboard.fill(self.GREY)
        width = self.window.get_size()[0] - self.window.get_size()[1]
        border = 10
        spacing = 5    
        line_height = self.font.size("I")[1]
        colour_box_size = math.ceil(line_height * 0.95)
        name_x = border + colour_box_size + spacing
        name_y = border
        score_x = width * 0.8        
        
        scores = self.world.get_score()
        max_score = self.world.grid.size
        sorted_scores = [  [   # Calculate all scores and sort the list
                        bot.get_name(), 
                        round(100*scores[bot.id]/max_score),
                        bot.id,
                    ]
                    for bot in self.world.bots]
        sorted_scores.sort(reverse=True, key=lambda e: e[1])

        for score in sorted_scores:
            bot_name, bot_score, bot_id = score
            # Draw colour square
            pygame.draw.rect(self.scoreboard, self.colour_from_id(bot_id), 
                             (border, name_y, colour_box_size, colour_box_size))
            
            # Draw number over the square
            if self.draw_bot_ids:
                font = pygame.font.SysFont(None, colour_box_size)
                text_to_render = f"{bot_id}"
                text = font.render(text_to_render, True, self.BLACK + (50,))
                text_size = font.size(text_to_render)
                self.scoreboard.blit(text, (
                    border + colour_box_size/2 - text_size[0]/2, 
                    name_y + colour_box_size/2 - text_size[1]/2
                    ))

            # Draw name
            text = self.font.render(f"{bot_name}", True, self.BLACK)
            self.scoreboard.blit(text, (name_x, name_y))

            # Draw score
            text = self.font.render(f"{bot_score} %", True, self.BLACK)
            self.scoreboard.blit(text, (score_x, name_y))

            # Update write location
            name_y += line_height + spacing
        self.window.blit(self.scoreboard, (self.window.get_size()[1], 0))

        # Draw the buttons (also on the scoreboard)
        button_font = pygame.font.SysFont(None, math.ceil(self.buttons[0].size[1] * 0.8))
        for button in self.buttons:
            pygame.draw.rect(self.window, self.BUTTON, (*button.position, *button.size))
            text_size = button_font.size(button.text)
            text = button_font.render(button.text, True, self.BLACK)
            text_size = button_font.size(button.text)
            self.window.blit(text, (
                    button.position[0] + button.size[0]/2 - text_size[0]/2, 
                    button.position[1] + button.size[1]/2 - text_size[1]/2))
        
        # Print some stats
        ref_button = self.buttons[0]
        ll_position = (ref_button.position[0], ref_button.position[1] - 10)
        text_to_render = "Round: {:<4}/{:<4}".format(self.world.game_info.current_round, self.world.game_info.number_of_rounds)
        text = button_font.render(text_to_render, True, self.BLACK)
        text_size = button_font.size(text_to_render)
        self.window.blit(text, (ll_position[0], ll_position[1] - text_size[1]/2))

    def handle_click(self, mouse):
        for button in self.buttons:
            if button.is_at_position(mouse):
                button.callback()
                return