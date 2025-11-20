from sqlmodel import Session
from app.services.employee_services import save_employees


class BaseHRISClient:
    def authenticate(self, provider):
        raise NotImplementedError

    def fetch_employees(self):
        raise NotImplementedError

    def transform(self, employee, mapping):
        raise NotImplementedError

    def sync(self, provider, db: Session, config=None):
        self.authenticate(provider)

        data = self.fetch_employees()

        mapping = (config or {}).get("field_mapping") or self.get_mapping()

        transformed = self.transform(data, mapping)
        save_employees(db, provider.id, transformed)

        return transformed
