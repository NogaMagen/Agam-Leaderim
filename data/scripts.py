import csv
from typing import Type
import io


from data_layer import SessionLocal
from models import Employee, Employer


class PopulateDataBase:
    def __init__(self):
        self._db = SessionLocal

    def populate_from_csv(self, model: Type, csv_file_path: str):
        with open(csv_file_path, "rb") as csvfile:
            text_file = io.TextIOWrapper(csvfile, encoding="utf-8-sig")
            reader = csv.DictReader(text_file)
            for row in reader:
                instance = model(**row)
                print(instance)
                self._db.add(instance)
            self._db.commit()
            self._db.refresh()

    def populate_employees(self):
        self.populate_from_csv(model=Employee, csv_file_path="employees.csv")

    def populate_employers(self):
        self.populate_from_csv(model=Employer, csv_file_path="employers.csv")
