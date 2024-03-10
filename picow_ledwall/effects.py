class Scroll:
    def __init__(self, ledwall, obj, speed=1):
        self.ledwall = ledwall
        self.obj = obj
        self.speed = speed
        self._scroll()

    def _scroll(self):
        for i in range(len(self.obj)):
            self.ledwall.display(self.obj, wait=1/self.speed)
            self.obj.position = (self.obj.position[0] - 1, self.obj.position[1])
