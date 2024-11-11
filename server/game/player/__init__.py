from ...proto.game import Record

class PlayerManager:
    def __init__(self, saving: Record):
        self.pid = saving.pid
        self.name = saving.name
        self.create_timne = saving.create_time
        self.type = saving.type
        self.level = saving.level
        self.saving = saving