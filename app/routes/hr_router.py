from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import shutil
import os
from pathlib import Path
from ..database import get_db
from ..models import models
from ..schemas import schemas
from datetime import datetime

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(
    prefix="/hr",
    tags=["HR"]
)

# Department routes
@router.post("/departments/", response_model=schemas.Department, status_code=status.HTTP_201_CREATED)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    try:
        db_dept = models.Department(
            title=department.title,
            description=department.description,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(db_dept)
        db.commit()
        db.refresh(db_dept)
        return db_dept
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/departments/", response_model=List[schemas.Department])
def list_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    departments = db.query(models.Department).offset(skip).limit(limit).all()
    return departments

@router.get("/departments/{department_id}", response_model=schemas.Department)
def get_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(models.Department).filter(models.Department.department_id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.patch("/departments/{department_id}", response_model=schemas.Department)
def update_department(department_id: int, department: schemas.DepartmentUpdate, db: Session = Depends(get_db)):
    db_dept = db.query(models.Department).filter(models.Department.department_id == department_id).first()
    if not db_dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    for key, value in department.dict(exclude_unset=True).items():
        setattr(db_dept, key, value)
    
    db.commit()
    db.refresh(db_dept)
    return db_dept

@router.delete("/departments/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    db_dept = db.query(models.Department).filter(models.Department.department_id == department_id).first()
    if not db_dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    db.delete(db_dept)
    db.commit()
    return {"ok": True}

# Position routes
@router.post("/positions/", response_model=schemas.Position)
def create_position(position: schemas.PositionCreate, db: Session = Depends(get_db)):
    # Verify department exists
    department = db.query(models.Department).filter(models.Department.department_id == position.department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    db_position = models.Position(**position.dict())
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position

@router.get("/positions/", response_model=List[schemas.Position])
def list_positions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    positions = db.query(models.Position).offset(skip).limit(limit).all()
    return positions

@router.patch("/positions/{position_id}", response_model=schemas.Position)  # Changed from designation_id
def update_position(
    position_id: int,  # Changed parameter name
    position: schemas.PositionUpdate,
    db: Session = Depends(get_db)
):
    db_position = db.query(models.Position).filter(models.Position.position_id == position_id).first()  # Updated field name
    if not db_position:
        raise HTTPException(status_code=404, detail="Position not found")
    
    if position.department_id:
        department = db.query(models.Department).filter(models.Department.department_id == position.department_id).first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
    
    for key, value in position.dict(exclude_unset=True).items():
        setattr(db_position, key, value)
    
    db.commit()
    db.refresh(db_position)
    return db_position

# Employee routes
@router.post("/employees/", response_model=schemas.Employee, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get("/employees/", response_model=List[schemas.Employee])
def list_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = db.query(models.Employee).offset(skip).limit(limit).all()
    return employees

@router.get("/employees/{employee_id}", response_model=schemas.Employee)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.patch("/employees/{employee_id}", response_model=schemas.Employee)
def update_employee(employee_id: int, employee: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    for key, value in employee.dict(exclude_unset=True).items():
        setattr(db_employee, key, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_employee)
    db.commit()
    return {"ok": True}

# Document routes
@router.post("/documents/", response_model=schemas.Document)
def create_document(document: schemas.DocumentCreate, db: Session = Depends(get_db)):
    db_document = models.Document(**document.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

@router.get("/documents/", response_model=List[schemas.Document])
def list_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    documents = db.query(models.Document).offset(skip).limit(limit).all()
    return documents

@router.post("/employees/{employee_id}/documents/", response_model=schemas.EmployeeDocument)
async def upload_employee_document(
    employee_id: int,
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Verify employee exists
    employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Create safe filename
    file_path = UPLOAD_DIR / f"{employee_id}_{document_type}_{file.filename}"
    
    # Save file
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not upload file: {str(e)}")
    
    # Create document record
    db_document = models.EmployeeDocument(
        employee_id=employee_id,
        document_type=document_type,
        document_path=str(file_path)
    )
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return db_document

@router.get("/employees/{employee_id}/documents/", response_model=List[schemas.EmployeeDocument])
def get_employee_documents(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return employee.documents

@router.get("/employees/{employee_id}/documents/{document_id}")
async def get_document(
    employee_id: int,
    document_id: int,
    db: Session = Depends(get_db)
):
    document = db.query(models.EmployeeDocument).filter(
        models.EmployeeDocument.document_id == document_id,
        models.EmployeeDocument.employee_id == employee_id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    file_path = Path(document.document_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Document file not found")
    
    return FileResponse(file_path)

# Search endpoints
@router.get("/departments/search/", response_model=List[schemas.Department])
def search_departments(
    query: str = Query(None, description="Search in title and description"),
    db: Session = Depends(get_db)
):
    search = f"%{query}%"
    departments = db.query(models.Department).filter(
        or_(
            models.Department.title.ilike(search),
            models.Department.description.ilike(search)
        )
    ).all()
    return departments

@router.get("/positions/search/", response_model=List[schemas.Position])
def search_positions(
    title: Optional[str] = Query(None, description="Search by title"),
    min_salary: Optional[float] = Query(None, description="Minimum salary range"),
    max_salary: Optional[float] = Query(None, description="Maximum salary range"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Position)
    
    if title:
        query = query.filter(models.Position.title.ilike(f"%{title}%"))
    if min_salary:
        query = query.filter(models.Position.salary_range_min >= min_salary)
    if max_salary:
        query = query.filter(models.Position.salary_range_max <= max_salary)
    
    return query.all()

@router.get("/employees/search/", response_model=List[schemas.Employee])
def search_employees(
    name: Optional[str] = Query(None, description="Search in first_name and last_name"),
    email: Optional[str] = Query(None, description="Search by email"),
    department_id: Optional[int] = Query(None, description="Filter by department"),
    position_id: Optional[int] = Query(None, description="Filter by position"),  # Changed from designation_id
    employment_type: Optional[str] = Query(None, description="Filter by employment type"),
    work_type: Optional[str] = Query(None, description="Filter by work type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Employee)
    
    if name:
        search = f"%{name}%"
        query = query.filter(
            or_(
                models.Employee.first_name.ilike(search),
                models.Employee.last_name.ilike(search)
            )
        )
    if email:
        query = query.filter(models.Employee.email.ilike(f"%{email}%"))
    if department_id:
        query = query.filter(models.Employee.department_id == department_id)
    if position_id:  # Changed from designation_id
        query = query.filter(models.Employee.position_id == position_id)
    if employment_type:
        query = query.filter(models.Employee.employment_type == employment_type)
    if work_type:
        query = query.filter(models.Employee.work_type == work_type)
    if status:
        query = query.filter(models.Employee.status == status)
    
    return query.all()

# Advanced search endpoint for employees with multiple fields and sorting
@router.get("/employees/advanced-search/", response_model=List[schemas.Employee])
def advanced_search_employees(
    search: Optional[str] = Query(None, description="Global search across name, email, phone"),
    department_ids: Optional[List[int]] = Query(None, description="Filter by multiple departments"),
    position_ids: Optional[List[int]] = Query(None, description="Filter by multiple positions"),  # Changed from designation_ids
    employment_types: Optional[List[str]] = Query(None, description="Filter by multiple employment types"),
    work_types: Optional[List[str]] = Query(None, description="Filter by multiple work types"),
    statuses: Optional[List[str]] = Query(None, description="Filter by multiple statuses"),
    sort_by: Optional[str] = Query("last_name", description="Field to sort by"),
    sort_desc: bool = Query(False, description="Sort in descending order"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.Employee)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.Employee.first_name.ilike(search_term),
                models.Employee.last_name.ilike(search_term),
                models.Employee.email.ilike(search_term),
                models.Employee.phone.ilike(search_term)
            )
        )
    
    if department_ids:
        query = query.filter(models.Employee.department_id.in_(department_ids))
    if position_ids:  # Changed from designation_ids
        query = query.filter(models.Employee.position_id.in_(position_ids))
    if employment_types:
        query = query.filter(models.Employee.employment_type.in_(employment_types))
    if work_types:
        query = query.filter(models.Employee.work_type.in_(work_types))
    if statuses:
        query = query.filter(models.Employee.status.in_(statuses))
    
    # Dynamic sorting
    sort_column = getattr(models.Employee, sort_by, models.Employee.last_name)
    if sort_desc:
        sort_column = sort_column.desc()
    
    query = query.order_by(sort_column)
    
    return query.offset(skip).limit(limit).all()
