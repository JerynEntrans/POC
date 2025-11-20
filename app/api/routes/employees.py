from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlmodel import Session

from app.core.database import get_db
from app.schemas.employee import EmployeeRead, EmployeeUpdate
from app.services.employee_services import (
    get_employee,
    get_employees_by_provider,
    update_employee,
    delete_employee,
)


router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee_endpoint(employee_id: UUID, db: Session = Depends(get_db)):
    employee = get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.get("/provider/{provider_id}", response_model=list[EmployeeRead])
def get_employees_by_provider_endpoint(provider_id: UUID, db: Session = Depends(get_db)):
    return get_employees_by_provider(db, provider_id)


@router.patch("/{employee_id}", response_model=EmployeeRead)
def update_employee_endpoint(
    employee_id: UUID,
    data: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    update_data = data.model_dump(exclude_unset=True)
    employee = update_employee(db, employee_id, update_data)

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee


@router.delete("/{employee_id}")
def delete_employee_endpoint(employee_id: UUID, db: Session = Depends(get_db)):
    success = delete_employee(db, employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"status": "success", "message": "Employee deleted"}
