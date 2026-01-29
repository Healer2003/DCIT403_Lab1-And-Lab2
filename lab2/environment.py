import random

class Environment:
    def __init__(self):
        self.disaster_types = ["Flood", "Earthquake", "Fire","Tsunami","Hurricane"]

    def generate_event(self):
        disaster = random.choice(self.disaster_types)
        severity = random.randint(1, 10)
        return {"disaster": disaster, "severity": severity}
