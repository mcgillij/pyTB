""" Basic MapTile container for tile data """


class MapTile:
    """MapTile class, generic class for a tile"""

    def __init__(self, value):
        self.value = value
        self.blocked = True
        self.blocked_sight = True
        self.fog = True
        self.content = []
