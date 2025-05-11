from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Float, Enum, Text, Boolean, Numeric, LargeBinary
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime
import enum

class Gender(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"

class MaritalStatus(str, enum.Enum):
    single = "single"
    married = "married"
    divorced = "divorced"
    widowed = "widowed"

class EmploymentType(str, enum.Enum):
    full_time = "full-time"
    part_time = "part-time"
    contract = "contract"
    intern = "intern"

class WorkType(str, enum.Enum):
    office = "office"
    remote = "remote"
    hybrid = "hybrid"

class EmployeeStatus(str, enum.Enum):
    active = "active"
    on_leave = "on_leave"
    resigned = "resigned"
    terminated = "terminated"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=False, index=True)
    name = Column(String)
    password = Column(String)  # Хранит хэш пароля
    created_at = Column(DateTime, default=datetime.utcnow)

class Department(Base):
    __tablename__ = "departments"
    
    department_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)  # Explicitly make it nullable
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    employees = relationship("Employee", back_populates="department", cascade="all, delete")
    positions = relationship("Position", back_populates="department", cascade="all, delete")

# Remove entire Designation class

class Position(Base):
    __tablename__ = "positions"
    
    position_id = Column(Integer, primary_key=True, index=True)  # Changed from designation_id
    title = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    department = relationship("Department", back_populates="positions")
    employees = relationship("Employee", back_populates="position")

class EmployeeDocument(Base):
    __tablename__ = "employee_documents"
    
    document_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    document_type = Column(String(50), nullable=False)
    document_path = Column(String(255), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    employee = relationship("Employee", back_populates="documents")

class Employee(Base):
    __tablename__ = "employees"
    
    employee_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    date_of_birth = Column(Date)
    gender = Column(Enum(Gender))
    marital_status = Column(Enum(MaritalStatus))
    address = Column(Text)
    city = Column(String(50))
    employment_type = Column(Enum(EmploymentType))
    work_type = Column(Enum(WorkType))
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    position_id = Column(Integer, ForeignKey("positions.position_id"))  # Updated to match new column name
    working_days = Column(String(20))
    join_date = Column(Date)
    ctc = Column(Numeric(12, 2))
    monthly_salary = Column(Numeric(10, 2))
    status = Column(Enum(EmployeeStatus), default=EmployeeStatus.active)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Update relationships
    department = relationship("Department", back_populates="employees")
    position = relationship("Position", back_populates="employees")
    documents = relationship("EmployeeDocument", back_populates="employee", cascade="all, delete")  # Changed from Document to EmployeeDocument
    # Removed designation relationship

# Optional: If you're not using the Document model, you can remove it
# If you are using it, update its relationship
class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)  # passport, contract, certificate, etc.
    number = Column(String)
    issue_date = Column(Date)
    expiry_date = Column(Date)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    employee = relationship("Employee")  # Remove back_populates here