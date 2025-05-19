from datetime import datetime
import uuid

class Checklist:
    def __init__(self, title_cl, e1, e2, e3):
        self.id = uuid.uuid4()
        self.title_cl = title_cl
        self.e1 = e1
        self.tick1 = False
        self.e2 = e2
        self.tick2 = False
        self.e3 = e3
        self.tick3 = False
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "title_cl": str(self.title_cl),
            "e1": str(self.e1),
            "e2": str(self.e2),
            "e3": str(self.e3),
            "created_at": str(self.created_at.isoformat()),
            "tick1": self.tick1,
            "tick2": self.tick2,
            "tick3": self.tick3
        }