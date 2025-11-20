from sqlalchemy import text, select
from sqlmodel import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate
from uuid import UUID


def save_employees(db: Session, provider_id: UUID, employees: list[dict]):

    for emp in employees:
        emp["provider_id"] = provider_id

        emp_schema = EmployeeCreate(**emp)
        params = emp_schema.model_dump()

        upsert_sql = text("""
            INSERT INTO employee (
                provider_id, employee_id, first_name, last_name, preferred_name,
                display_name, job_title, location, supervisor, department,
                division, work_email, work_phone, work_phone_extension, photo_url
            )
            VALUES (
                :provider_id, :employee_id, :first_name, :last_name, :preferred_name,
                :display_name, :job_title, :location, :supervisor, :department,
                :division, :work_email, :work_phone, :work_phone_extension, :photo_url
            )
            ON CONFLICT (provider_id, employee_id)
            DO UPDATE SET
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                preferred_name = EXCLUDED.preferred_name,
                display_name = EXCLUDED.display_name,
                job_title = EXCLUDED.job_title,
                location = EXCLUDED.location,
                supervisor = EXCLUDED.supervisor,
                department = EXCLUDED.department,
                division = EXCLUDED.division,
                work_email = EXCLUDED.work_email,
                work_phone = EXCLUDED.work_phone,
                work_phone_extension = EXCLUDED.work_phone_extension,
                photo_url = EXCLUDED.photo_url,
                updated_at = NOW();
        """)

        db.exec(upsert_sql, params=params)

    db.commit()


def create_employee(db: Session, data: EmployeeCreate) -> Employee:
    employee = Employee(**data.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def get_employee(db: Session, employee_id: UUID) -> Employee | None:
    return db.get(Employee, employee_id)


def get_employees_by_provider(db: Session, provider_id: UUID):
    return db.exec(
        select(Employee).where(Employee.provider_id == provider_id)
    ).scalars().all()


def update_employee(db: Session, employee_id: UUID, data: dict) -> Employee | None:
    employee = db.get(Employee, employee_id)
    if not employee:
        return None

    for key, value in data.items():
        setattr(employee, key, value)

    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def delete_employee(db: Session, employee_id: UUID) -> bool:
    employee = db.get(Employee, employee_id)
    if not employee:
        return False
    db.delete(employee)
    db.commit()
    return True
