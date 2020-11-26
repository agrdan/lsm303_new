

class WindowStatusDto:

    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        self.vector = None
        self.status = None
        self.statusName = None


    def fromEntity(self, windowEntity):
        self.x = windowEntity.x
        self.y = windowEntity.y
        self.z = windowEntity.z
        self.vector = windowEntity.vector
        self.status = windowEntity.status
        if windowEntity.status == 1:
            self.statusName = 'otvoren'
        elif windowEntity.status == 2:
            self.statusName = 'zatvoren'
        elif windowEntity.status == 3:
            self.statusName = 'kip'
