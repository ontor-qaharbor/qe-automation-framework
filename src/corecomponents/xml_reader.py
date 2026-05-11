from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET


class XmlReader:
    """XML read helpers."""

    @staticmethod
    def read(path: str | Path) -> ET.ElementTree:
        return ET.parse(str(path))

