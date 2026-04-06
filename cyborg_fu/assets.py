"""Asset loading utilities for images and sounds."""
# pylint: disable=no-member
from __future__ import annotations

from pathlib import Path

import pygame


def get_data_dir() -> Path:
    """Return the path to the data/ directory containing game assets."""
    return Path(__file__).resolve().parent.parent / "data"


def load_png(name: str) -> tuple[pygame.Surface, pygame.Rect]:
    """Load a PNG image and return (surface, rect).

    Handles alpha conversion automatically.
    """
    fullname = get_data_dir() / name
    try:
        image: pygame.Surface = pygame.image.load(str(fullname))
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print(f"Cannot load image: {fullname}")
        raise SystemExit(f"Cannot load image: {fullname}") from message
    rect: pygame.Rect = image.get_rect()
    return image, rect


def load_image(name: str) -> pygame.Surface:
    """Load an image file and return the surface (no rect).

    Used for backgrounds and tiles.
    """
    fullname = get_data_dir() / name
    try:
        surface: pygame.Surface = pygame.image.load(str(fullname))
    except pygame.error as message:
        raise SystemExit(
            f'Could not load image "{fullname}": {pygame.get_error()}'
        ) from message
    return surface.convert()
