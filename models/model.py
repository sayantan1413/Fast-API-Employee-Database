from pydantic import BaseModel


class Employee(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    salary: float
