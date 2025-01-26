import csv
import io
from typing import Type

from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError

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
            government_id = row.get("government_id")
            existing_instance = self._db.query(model).filter_by(government_id=government_id).first()

            if existing_instance:
                continue

            try:
                instance = model(**row)
                self._db.add(instance)
            except IntegrityError as e:
                self._db.rollback()

        try:
            self._db.commit()
        except IntegrityError as e:
            self._db.rollback()
        finally:
            self._db.refresh()

    async def populate_employees(self, file: UploadFile):
        await self.populate_from_csv(model=Employee, file=file)

    async def populate_employers(self, file: UploadFile):
        await self.populate_from_csv(model=Employer, file=file)
