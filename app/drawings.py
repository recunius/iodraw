import logging
import datetime
from lru import LRU

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Drawings:

    def __init__(self, max_active):
        self.drawings = LRU(max_active)
    
    def get_drawing(self, room):
        for (k, v) in self.drawings.items():
            logger.debug('{}: {} (len {})'.format(id(self), k , len(v)))
        try:
            d = self.drawings[room]
        except KeyError:
            d = self.drawings[room] = [ ]
        return d
