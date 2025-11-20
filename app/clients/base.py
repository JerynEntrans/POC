class BaseHRISClient:
    def authenticate(self, provider, config):
        raise NotImplementedError

    def fetch_employees(self):
        raise NotImplementedError

    def transform(self, employee, mapping):
        raise NotImplementedError

    def sync(self, provider, config=None):
        self.authenticate(provider)

        data = self.fetch_employees()
        print(data)

        mapping = (config or {}).get("field_mapping") or self.get_mapping()
        print(mapping)

        transformed = self.transform(data, mapping)

        return transformed
