import csv
import io
from typing import Type

from fastapi import UploadFile

from data_layer import SessionLocal
from models import Employee, Employer


class PopulateService:
    def __init__(self):
        self._db = SessionLocal

    async def populate_from_csv(self, model: Type, file: UploadFile):
        content = await file.read()
        text_file = io.TextIOWrapper(io.BytesIO(content), encoding="utf-8-sig")
        reader = csv.DictReader(text_file)

        for row in reader:
            instance = model(**row)
            self._db.add(instance)

        self._db.commit()
        self._db.refresh()

    async def populate_employees(self, file: UploadFile):
        await self.populate_from_csv(model=Employee, file=file)

    async def populate_employers(self, file: UploadFile):
        await self.populate_from_csv(model=Employer, file=file)
