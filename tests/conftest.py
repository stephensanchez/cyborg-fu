"""Shared test fixtures for Cyborg-Fu tests."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def mock_pygame() -> Any:
    """Mock pygame.display and pygame.image for all tests."""
    mock_surface = MagicMock()
    mock_surface.get_rect.return_value = MagicMock(
        left=0, right=800, top=0, bottom=600, width=800, height=600,
        contains=MagicMock(return_value=True),
    )
    mock_surface.get_size.return_value = (800, 600)

    mock_image = MagicMock()
    mock_rect = MagicMock()
    mock_rect.move.return_value = mock_rect
    mock_rect.left = 100
    mock_rect.right = 130
    mock_rect.top = 100
    mock_rect.bottom = 130
    mock_rect.center = (115, 115)
    mock_rect.midtop = (115, 100)
    mock_rect.midbottom = (115, 130)
    mock_rect.midleft = (100, 115)
    mock_rect.midright = (130, 115)
    mock_image.get_rect.return_value = mock_rect
    mock_image.get_alpha.return_value = None

    with (
        patch("pygame.init"),
        patch("pygame.display.get_surface", return_value=mock_surface),
        patch("pygame.display.set_mode", return_value=mock_surface),
        patch("pygame.display.mode_ok", return_value=32),
        patch("pygame.display.set_caption"),
        patch("pygame.display.flip"),
        patch("pygame.image.load", return_value=mock_image),
        patch("pygame.event.pump"),
        patch("pygame.font.Font", return_value=MagicMock(
            render=MagicMock(return_value=mock_image),
        )),
        patch("pygame.transform.rotate", return_value=mock_image),
        patch("pygame.transform.scale", return_value=mock_image),
        patch("pygame.Surface", return_value=mock_surface),
    ):
        yield mock_surface
