class Scroll:
    def __init__(self, ledwall, obj, speed=1, direction="left"):
        self.ledwall = ledwall
        self.obj = obj
        self.speed = speed
        self._scroll(direction=direction)

    def _scroll(self, direction):
        """scroll object by changing its position attribute."""
        if direction == "left":
            motion = (-1, 0)
        elif direction == "right":
            motion = (1, 0)
        elif direction == "up":
            motion = (0, -1)
        elif direction == "down":
            motion = (0, 1)
        else:
            raise ValueError("direction must be 'left', 'right', 'up', or 'down'.")

        # move the object
        for i in range(len(self.obj)):
            # speed is the inverse of the frame rate
            self.ledwall.display(self.obj, wait=1 / self.speed)
            # set the new position
            self.obj.position = (
                self.obj.position[0] + motion[0],
                self.obj.position[1] + motion[1],
            )
