from pydantic import BaseModel
from typing import Optional

import datetime
from datetime import timedelta

counter=1


class SimplePacjent(BaseModel):
    name: str
    surname: str


class Pacjent:
    def __init__(self, podstawa: SimplePacjent):
        global counter
        self.id = counter
        counter += 1
        self.name = podstawa.name
        self.surname = podstawa.surname
        self.register_date = datetime.date.today()
        self.vaccination_date = self.register_date + timedelta(days=(len(self.name)+len(self.surname)))