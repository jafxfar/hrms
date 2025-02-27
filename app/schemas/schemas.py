from pydantic import BaseModel, EmailStr, validator
from datetime import datetime, date
from typing import Optional, List
from enum import Enum
import os

# Enums
class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class MaritalStatusEnum(str, Enum):
    single = "single"
    married = "married"
    divorced = "divorced"
    widowed = "widowed"

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class DepartmentBase(BaseModel):
    title: str
    description: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    department_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DepartmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class PositionBase(BaseModel):
    title: str
    department_id: int
    description: Optional[str] = None

class PositionCreate(PositionBase):
    pass

class Position(PositionBase):
    position_id: int  # Changed from designation_id
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PositionUpdate(BaseModel):
    title: Optional[str] = None
    department_id: Optional[int] = None
    description: Optional[str] = None

class EmployeeDocumentBase(BaseModel):
    document_type: str
    document_path: str

class EmployeeDocumentCreate(EmployeeDocumentBase):
    pass

class EmployeeDocument(EmployeeDocumentBase):
    document_id: int
    employee_id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[GenderEnum] = None
    marital_status: Optional[MaritalStatusEnum] = None
    address: Optional[str] = None
    city: Optional[str] = None
    employment_type: str
    work_type: str
    department_id: int
    position_id: int  # Changed from optional to required
    working_days: Optional[str] = None
    join_date: date
    ctc: Optional[float] = None
    monthly_salary: Optional[float] = None
    # Removed designation_id

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    employee_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    documents: List['Document'] = []

    class Config:
        from_attributes = True

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    marital_status: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    employment_type: Optional[str] = None
    work_type: Optional[str] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    # Removed designation_id field
    working_days: Optional[str] = None
    monthly_salary: Optional[float] = None
    status: Optional[str] = None
    ctc: Optional[float] = None

    class Config:
        from_attributes = True

class DocumentBase(BaseModel):
    title: str
    type: str
    number: Optional[str] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    employee_id: int

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    created_at: datetime
    employee: Optional['Employee'] = None

    class Config:
        from_attributes = True

# Add this at the end of the file to resolve forward references
Employee.model_rebuild()
Document.model_rebuild()