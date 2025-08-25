import httpx
import asyncio
from typing import List, Dict, Any
from datetime import datetime, date
from app.domain.entities.patient import Patient
from app.domain.interfaces import ISyntheaService
from app.config import settings

class SyntheaService(ISyntheaService):
    def __init__(self):
        self._base_url = settings.synthea_base_url
        self._timeout = 30
        
    async def fetch_patients(self, count: int = 10) -> List[Dict[str, Any]]:
        synthea_data = [
            {
                "resourceType": "Patient",
                "id": "synthea-001",
                "name": [{"family": "Doe", "given": ["John", "Michael"]}],
                "gender": "male",
                "birthDate": "1990-01-15",
                "address": [{
                    "line": ["123 Main St"],
                    "city": "Boston",
                    "state": "MA",
                    "postalCode": "02101"
                }],
                "telecom": [{
                    "system": "phone",
                    "value": "555-0123"
                }, {
                    "system": "email",
                    "value": "john.doe@example.com"
                }],
                "extension": [{
                    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
                    "valueCodeableConcept": {
                        "coding": [{"display": "White"}]
                    }
                }, {
                    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
                    "valueCodeableConcept": {
                        "coding": [{"display": "Not Hispanic or Latino"}]
                    }
                }],
                "identifier": [{
                    "type": {"coding": [{"code": "SS"}]},
                    "value": "999-12-3456"
                }]
            },
            {
                "resourceType": "Patient",
                "id": "synthea-002",
                "name": [{"family": "Smith", "given": ["Jane", "Elizabeth"]}],
                "gender": "female",
                "birthDate": "1985-05-20",
                "address": [{
                    "line": ["456 Oak Ave"],
                    "city": "Cambridge",
                    "state": "MA",
                    "postalCode": "02139"
                }],
                "telecom": [{
                    "system": "phone",
                    "value": "555-0456"
                }, {
                    "system": "email",
                    "value": "jane.smith@example.com"
                }],
                "extension": [{
                    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
                    "valueCodeableConcept": {
                        "coding": [{"display": "Black or African American"}]
                    }
                }, {
                    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
                    "valueCodeableConcept": {
                        "coding": [{"display": "Not Hispanic or Latino"}]
                    }
                }],
                "identifier": [{
                    "type": {"coding": [{"code": "SS"}]},
                    "value": "999-65-4321"
                }]
            },
            {
                "resourceType": "Patient",
                "id": "synthea-003",
                "name": [{"family": "Garcia", "given": ["Carlos", "Antonio"]}],
                "gender": "male",
                "birthDate": "1978-11-08",
                "address": [{
                    "line": ["789 Pine St"],
                    "city": "Somerville",
                    "state": "MA",
                    "postalCode": "02143"
                }],
                "telecom": [{
                    "system": "phone",
                    "value": "555-0789"
                }, {
                    "system": "email",
                    "value": "carlos.garcia@example.com"
                }],
                "extension": [{
                    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
                    "valueCodeableConcept": {
                        "coding": [{"display": "Other"}]
                    }
                }, {
                    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
                    "valueCodeableConcept": {
                        "coding": [{"display": "Hispanic or Latino"}]
                    }
                }],
                "identifier": [{
                    "type": {"coding": [{"code": "SS"}]},
                    "value": "999-87-6543"
                }]
            }
        ]
        
        return synthea_data[:count]
    
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
