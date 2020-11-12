class Addvehicle(object):
    def __init__(self, startpos, startdirec, startvelo):
        self.position = startpos
        self.direction = startdirec
        self.velocity = startvelo
        self.neighbors = []
        self.destinations = []