from pydantic import BaseModel
from typing import Optional
import re
import datetime
from datetime import timedelta


class CategoriesDto(BaseModel):
    name: str


class SimplePacjent(BaseModel):
    name: str
    surname: str


class Pacjent:
    def __init__(self, podstawa: SimplePacjent, numer=None):
        regex = re.compile('[\W\d]')
        self.id = numer
        self.name = podstawa.name
        self.surname = podstawa.surname

        literyimie = len(regex.sub('', podstawa.name))
        literynazwisko = len(regex.sub('', podstawa.surname))
        # self.register_date = datetime.date(2021, 4, 1)
        self.register_date = datetime.date.today()
        self.vaccination_date = self.register_date + timedelta(days=(literyimie + literynazwisko))
