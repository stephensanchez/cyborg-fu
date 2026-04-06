"""Shared utilities for game stages."""
# pylint: disable=no-member
from __future__ import annotations
import pygame
from cyborg_fu.assets import load_image
from cyborg_fu.constants import SCREEN_HEIGHT, SCREEN_WIDTH


def create_screen(caption: str = "Cyborg-Fu!") -> tuple[pygame.Surface, pygame.Rect]:
    """Initialize pygame display and return (screen surface, screen rect)."""
    pygame.init()
    screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    bestdepth = pygame.display.mode_ok(screen_rect.size, 0, 32)
    screen = pygame.display.set_mode(screen_rect.size, 0, bestdepth)
    pygame.display.set_caption(caption)
    return screen, screen_rect


def create_tiled_background(tile_name: str, screen_rect: pygame.Rect) -> pygame.Surface:
    """Create a background surface by tiling an image."""
    tile = load_image(tile_name)
    background = pygame.Surface(screen_rect.size)
    for x in range(0, screen_rect.width, tile.get_width()):
        for y in range(0, screen_rect.height, tile.get_height()):
            background.blit(tile, (x, y))
    return background


def create_image_background(image_name: str, screen_rect: pygame.Rect) -> pygame.Surface:
    """Create a background from a single full-size image."""
    image = load_image(image_name)
    background = pygame.Surface(screen_rect.size)
    background.blit(image, (0, 0))
    return background
