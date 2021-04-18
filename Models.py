from pydantic import BaseModel
from typing import Optional
import re
import datetime
from datetime import timedelta

counter = 1


class SimplePacjent(BaseModel):
    name: str
    surname: str


class Pacjent:
    def __init__(self, podstawa: SimplePacjent):
        global counter
        regex = re.compile('[^a-zA-Z]')
        self.id = counter
        counter += 1
        self.name = podstawa.name
        self.surname = podstawa.surname

        literyimie = len(regex.sub('', podstawa.name))
        literynazwisko = len(regex.sub('', podstawa.surname))
        # self.register_date = datetime.date(2021, 4, 1)
        self.register_date = datetime.date.today()
        self.vaccination_date = self.register_date + timedelta(days=(literyimie+literynazwisko))
