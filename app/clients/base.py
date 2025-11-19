class BaseHRISClient:
    def authenticate(self, provider, config):
        raise NotImplementedError

    def fetch_employees(self):
        raise NotImplementedError

    def transform(self, employee, mapping):
        return {
            my: employee.get(their)
            for my, their in mapping.items()
        }

    def sync(self, provider, config):
        self.authenticate(provider, config)

        data = self.fetch_employees()

        mapping = config.get("field_mapping", {})

        transformed = [self.transform(emp, mapping) for emp in data]

        return transformed
