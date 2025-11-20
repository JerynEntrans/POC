from sqlmodel import Session
from sqlalchemy import text


def save_employees(db: Session, provider_id: str, employees: list[dict]):
    for emp in employees:
        emp["provider_id"] = provider_id

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

        db.exec(upsert_sql, params=emp)

    db.commit()
