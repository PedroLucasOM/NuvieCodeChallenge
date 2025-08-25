import httpx
import re
from typing import List, Dict, Any

class ExternalApiService:
    def __init__(self):
        self._base_url = "https://jsonplaceholder.typicode.com"
        self._timeout = httpx.Timeout(30.0)

    async def fetch_patients(self, count: int = 10) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.get(f"{self._base_url}/users")
            response.raise_for_status()
            users = response.json()[:count]
            
            return [
                {
                    "name": self._clean_name(user["name"]),
                    "email": user["email"],
                    "phone": self._clean_phone(user["phone"])
                }
                for user in users
            ]
    
    def _clean_name(self, name: str) -> str:
        """Clean name to match validation requirements: only letters, spaces, hyphens, apostrophes"""
        name = re.sub(r'\b(Mr|Mrs|Ms|Dr|Prof)\.?\s*', '', name)
        name = re.sub(r'\s+[A-Z]\.?$', '', name)
        name = re.sub(r'[^a-zA-Z\s\'-]', '', name)
        name = re.sub(r'\s+', ' ', name).strip()
        return name
    
    def _clean_phone(self, phone: str) -> str:
        """Extract main phone number without extensions"""
        phone = re.sub(r'\s*x\d+.*$', '', phone)
        return phone.split()[0] if phone else phone
