from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    government_id = Column(Integer, unique=True, nullable=False)

    employer_relationship = relationship("EmployersToEmployees", back_populates="employee")


class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    government_id = Column(Integer, unique=True, nullable=False)

    employee_relationships = relationship("EmployersToEmployees", back_populates="employer")


class EmployeeToEmployer(Base):
    __tablename__ = "employees_to_employers"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True, nullable=False)
    employer_id = Column(Integer, ForeignKey("employers.id"), nullable=False)

    employee = relationship("Employees", back_populates="employer_relationship")
    employer = relationship("Employers", back_populates="employee_relationships")
