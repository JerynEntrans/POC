import requests
from .base import BaseHRISClient


class BambooHRClient(BaseHRISClient):
    def get_mapping(self):
        return {
            "first_name": "firstName",
            "last_name": "lastName",
            "status": "status",
            "job_title": "jobTitleName",
            "employee_id": "employeeId",
            "location": "location",
        }

    def authenticate(self, provider):
        # BambooHR uses API Key as basic auth
        if not isinstance(provider.config, dict) or "api_key" not in provider.config or "subdomain" not in provider.config:
            raise ValueError("Invalid credentials for BambooHR provider")
        self.api_key = provider.config["api_key"]
        self.subdomain = provider.config["subdomain"]

        self.base_url = f"https://{self.subdomain}.bamboohr.com/api/v1/"

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def transform(self, data, mapping):
        data_to_transform = []
        if data and isinstance(data, dict) and "data" in data:
            data_to_transform = data["data"]

        return [{my: emp.get(their) for my, their in mapping.items()} for emp in data_to_transform if isinstance(emp, dict)]

    def fetch_employees(self):
        url = f"{self.base_url}employees"

        r = requests.get(
            url,
            auth=(self.api_key, "x"),
            headers=self.headers
        )
        r.raise_for_status()

        data = r.json()

        return data
