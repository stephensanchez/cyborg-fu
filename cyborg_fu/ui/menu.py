"""Main menu screen with hero selection."""
# pylint: disable=no-name-in-module,no-member
from __future__ import annotations

import pygame
from pygame.locals import K_DOWN, K_RETURN, K_SPACE, K_UP, KEYDOWN, QUIT

from cyborg_fu.constants import COLOR_BLACK, FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from cyborg_fu.ui.text import MenuText


def mainmenu() -> str | None:
    """Display the main menu and return the chosen hero type.

    Returns:
        "tesi" or "gunner", or None if the user quits.
    """
    pygame.init()
    screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    bestdepth = pygame.display.mode_ok(screen_rect.size, 0, 32)
    screen = pygame.display.set_mode(screen_rect.size, 0, bestdepth)
    pygame.display.set_caption("Cyborg-Fu!")

    background = pygame.Surface(screen_rect.size)
    background = background.convert()
    background.fill(COLOR_BLACK)

    welcome = MenuText("Welcome, to Cyborg-Fu.  (Press the space bar to continue)", 20, 10)
    arrow = MenuText("->", 20, 150)

    objects = pygame.sprite.Group(welcome)
    clock = pygame.time.Clock()

    choice = "sword"
    messages: list[MenuText] = [
        MenuText("You are a cyborg, programmed by me, the professor.", 20, 30),
        MenuText(
            "My work is complete, it is time to test you against some nasty little critters...",
            20, 50,
        ),
        MenuText(
            "To move, use the W, A, S, and D keys.  Your basic attack can be used by the spacebar.",
            20, 70,
        ),
        MenuText(
            "For each stage I present you, try and gain twenty points, then come speak to me.",
            20, 90,
        ),
        MenuText(
            "Press E through Y for possible special abilities, they will use your mana!",
            20, 110,
        ),
        MenuText("Which weapon do you prefer for battle?", 20, 130),
    ]

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return None
            if event.type == KEYDOWN:
                if event.key == K_SPACE and len(messages) > 0:
                    message = messages[0]
                    objects.add(message)
                    messages.remove(message)
                if event.key == K_DOWN and len(messages) == 0:
                    choice = "gun"
                    arrow.loc_y = 170
                if event.key == K_UP and len(messages) == 0:
                    choice = "sword"
                    arrow.loc_y = 150
                if event.key == K_RETURN and len(messages) == 0:
                    if choice == "sword":
                        return "tesi"
                    return "gunner"

        if len(messages) == 0:
            objects.add(MenuText("Sword", 50, 150))
            objects.add(MenuText("Gun", 50, 170))
            objects.add(MenuText("Use the up and down keys to select, then press enter.", 20, 190))
            objects.add(arrow)

        objects.clear(screen, background)
        objects.update()
        objects.draw(screen)
        pygame.display.flip()
