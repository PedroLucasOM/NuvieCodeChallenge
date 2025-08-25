import httpx
import asyncio
from typing import List, Dict, Any
from datetime import datetime, date
from app.domain.entities.patient import Patient
from app.domain.interfaces import ISyntheaService
from app.config import settings
import random

class SyntheaService(ISyntheaService):
    def __init__(self):
        self._base_url = "https://jsonplaceholder.typicode.com"
        self._timeout = 30
    
    async def fetch_patients(self, count: int = 10) -> List[Dict[str, Any]]:
        """Fetch real data from JSONPlaceholder API and transform to patient-like data"""
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            try:
                response = await client.get(f"{self._base_url}/users")
                response.raise_for_status()
                users_data = response.json()
                
                transformed_patients = []
                for i, user in enumerate(users_data[:count]):
                    patient_data = await self._transform_user_to_patient(user, i)
                    transformed_patients.append(patient_data)
                
                return transformed_patients
                
            except httpx.HTTPError as e:
                raise Exception(f"Failed to fetch data from external API: {str(e)}")
            except Exception as e:
                raise Exception(f"Error processing external data: {str(e)}")
    
    async def _transform_user_to_patient(self, user_data: Dict[str, Any], index: int) -> Dict[str, Any]:
        """Transform JSONPlaceholder user data to patient format"""
        genders = ["male", "female", "other"]
        races = ["white", "black", "asian", "hispanic", "other"]
        ethnicities = ["hispanic", "non-hispanic"]
        
        full_name = user_data.get("name", "Unknown User")
        name_parts = full_name.split()
        first_name = name_parts[0] if name_parts else "Unknown"
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else "User"
        
        birth_year = datetime.now().year - random.randint(25, 80)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        birth_date = f"{birth_year}-{birth_month:02d}-{birth_day:02d}"
        
        address_info = user_data.get("address", {})
        
        return {
            "resourceType": "Patient",
            "id": f"external-{user_data.get('id', index)}",
            "name": [{"family": last_name, "given": [first_name]}],
            "gender": random.choice(genders),
            "birthDate": birth_date,
            "address": [{
                "line": [address_info.get("street", "Unknown Street")],
                "city": address_info.get("city", "Unknown City"),
                "state": "MA",  # Default state
                "postalCode": address_info.get("zipcode", "00000")
            }],
            "telecom": [
                {
                    "system": "phone",
                    "value": user_data.get("phone", "555-0000")
                },
                {
                    "system": "email", 
                    "value": user_data.get("email", f"{first_name.lower()}@example.com")
                }
            ],
            "extension": [
                {
                    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
                    "valueCodeableConcept": {
                        "coding": [{"display": random.choice(races).title()}]
                    }
                },
                {
                    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity", 
                    "valueCodeableConcept": {
                        "coding": [{"display": random.choice(ethnicities).replace("-", " ").title()}]
                    }
                }
            ],
            "identifier": [
                {
                    "type": {"coding": [{"code": "SS"}]},
                    "value": f"999-{random.randint(10, 99)}-{random.randint(1000, 9999)}"
                }
            ]
        }

    async def transform_fhir_to_patient(self, fhir_data: Dict[str, Any]) -> Patient:
        names = fhir_data.get("name", [{}])[0]
        first_name = " ".join(names.get("given", []))
        last_name = names.get("family", "")
        
        birth_date_str = fhir_data.get("birthDate", "")
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date() if birth_date_str else date.today()
        
        address = fhir_data.get("address", [{}])[0] if fhir_data.get("address") else {}
        address_line = " ".join(address.get("line", [])) if address.get("line") else None
        
        telecoms = fhir_data.get("telecom", [])
        phone = None
        email = None
        
        for telecom in telecoms:
            if telecom.get("system") == "phone":
                phone = telecom.get("value")
            elif telecom.get("system") == "email":
                email = telecom.get("value")
        
        extensions = fhir_data.get("extension", [])
        race = None
        ethnicity = None
        
        for ext in extensions:
            if "us-core-race" in ext.get("url", ""):
                race_coding = ext.get("valueCodeableConcept", {}).get("coding", [{}])[0]
                race = race_coding.get("display")
            elif "us-core-ethnicity" in ext.get("url", ""):
                ethnicity_coding = ext.get("valueCodeableConcept", {}).get("coding", [{}])[0]
                ethnicity = ethnicity_coding.get("display")
        
        identifiers = fhir_data.get("identifier", [])
        ssn = None
        
        for identifier in identifiers:
            if identifier.get("type", {}).get("coding", [{}])[0].get("code") == "SS":
                ssn = identifier.get("value")
        
        return Patient(
            id=None,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=birth_date,
            gender=fhir_data.get("gender", "unknown"),
            ssn=ssn,
            address=address_line,
            city=address.get("city"),
            state=address.get("state"),
            zip_code=address.get("postalCode"),
            phone=phone,
            email=email,
            synthea_id=fhir_data.get("id"),
            race=race,
            ethnicity=ethnicity
        )
