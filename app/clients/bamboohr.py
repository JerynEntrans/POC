import requests
from .base import BaseHRISClient


class BambooHRClient(BaseHRISClient):
    def get_mapping(self):
        return {
            "first_name": "firstName",
            "last_name": "lastName",
            "preferred_name": "preferredName",
            "display_name": "displayName",
            "job_title": "jobTitle",
            "employee_id": "id",
            "location": "location",
            "supervisor": "supervisor",
            "department": "department",
            "division": "division",
            "work_email": "workEmail",
            "work_phone": "workPhone",
            "photo_url": "photoUrl",
            "work_phone_extension": "workPhoneExtension",
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

    def transform(self, data_to_transform, mapping):
        return [{my: emp.get(their) for my, their in mapping.items()} for emp in data_to_transform if isinstance(emp, dict)]

    def fetch_employees(self, initial_url=None):
        """
        Fetches employees from BambooHR API using pagination (`links.next`).
        Returns a flat list of employee dicts.
        """
        employees = []

        # Start with initial URL or default endpoint
        url = initial_url or f"{self.base_url}employees/directory"

        while url:
            r = requests.get(
                url,
                auth=(self.api_key, "x"),
                headers=self.headers
            )
            r.raise_for_status()

            data = r.json()

            # Collect data
            if isinstance(data, dict):
                if "employees" in data and isinstance(data["employees"], list):
                    employees.extend(data["employees"])

                # Pagination
                next_url = data.get("links", {}).get("next")
                url = next_url
            else:
                break
        return employees
