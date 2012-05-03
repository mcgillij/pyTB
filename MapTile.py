try:
    import sys
    
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)

class MapTile():
    """ MapTile class, generic class for a tile """
    def __init__(self, value):
        self.value = value
        self.blocked = True
        self.blocked_sight = True
        self.fog = True
        self.content = []