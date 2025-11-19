import requests
from .base import BaseHRISClient


class BambooHRClient(BaseHRISClient):

    def authenticate(self, provider, config):
        # BambooHR uses API Key as basic auth
        self.api_key = provider.creds["api_key"]
        self.subdomain = provider.creds["subdomain"]

        self.base_url = f"https://api.bamboohr.com/api/gateway.php/{self.subdomain}/v1"

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def fetch_employees(self):
        url = f"{self.base_url}/employees/directory"

        r = requests.get(
            url,
            auth=(self.api_key, "x"),
            headers=self.headers
        )
        r.raise_for_status()

        data = r.json()

        return data.get("employees", [])
