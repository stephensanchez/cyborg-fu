"""Tests for asset loading utilities."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from cyborg_fu.assets import get_data_dir, load_image, load_png


class TestGetDataDir:
    def test_returns_path(self) -> None:
        result = get_data_dir()
        assert isinstance(result, Path)

    def test_path_ends_with_data(self) -> None:
        result = get_data_dir()
        assert result.name == "data"


class TestLoadPng:
    def test_returns_image_and_rect(self) -> None:
        image, rect = load_png("hero.png")
        assert image is not None
        assert rect is not None


class TestLoadImage:
    def test_returns_surface(self) -> None:
        result = load_image("graytile.png")
        assert result is not None
