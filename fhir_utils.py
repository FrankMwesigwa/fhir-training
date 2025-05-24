import uuid
from datetime import datetime

def generate_id():
    return str(uuid.uuid4())

def create_patient_resource(patient_data):
    return {
        "resourceType": "Patient",
        "id": generate_id(),
        "active": True,
        "name": [{
            "given": list(filter(None, [patient_data.get("firstname"), patient_data.get("middlename")])),
            "family": patient_data.get("lastname")
        }],
        "gender": patient_data.get("gender", "unknown").lower(),
        "birthDate": patient_data.get("dob"),
        "identifier": [
            {
                "system": "http://fhir.health.go.ug/nationalId",
                "value": patient_data.get("nationalId")
            },
            {
                "system": "http://fhir.health.go.ug/passport",
                "value": patient_data.get("passport", "")
            },
            {
                "system": "http://fhir.health.go.ug/emrId",
                "value": patient_data.get("emrId")
            }
        ],
        "telecom": [
            {
                "system": "phone",
                "value": patient_data.get("phoneNumber"),
                "use": "home"
            },
            {
                "system": "email",
                "value": patient_data.get("email"),
                "use": "home"
            }
        ],
        "address": [{
            "line": [patient_data.get("address", "")],
            "city": patient_data.get("city", ""),
            "postalCode": patient_data.get("postalCode", ""),
            "extension": [{
                "url": "http://fhir.health.go.ug/ext/address",
                "extension": [
                    {"url": "http://fhir.health.go.ug/ext/address#district", "valueString": patient_data.get("district", "")},
                    {"url": "http://fhir.health.go.ug/ext/address#subcounty", "valueString": patient_data.get("subcounty", "")},
                    {"url": "http://fhir.health.go.ug/ext/address#parish", "valueString": patient_data.get("parish", "")},
                    {"url": "http://fhir.health.go.ug/ext/address#village", "valueString": patient_data.get("village", "")}
                ]
            }]
        }],
        "managingOrganization": {
            "reference": "Organization/8",
            "identifier": {
                "system": "https://hmis.health.go.ug/",
                "use": "official",
                "value": "BrtC10sqp45"
            },
            "display": "Kawempe National Referral Hospital"
        }
    }

def create_encounter_resource(encounter_data, patient_id):
    return {
        "resourceType": "Encounter",
        "id": generate_id(),
        "status": "finished",
        "class": {
            "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
            "code": "AMB",
            "display": "ambulatory"
        },
        "type": [
            {
                "text": encounter_data.get("encounter_type", "Outpatient Consultation")
            }
        ],
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "period": {
            "start": encounter_data.get("start"),
            "end": encounter_data.get("end")
        },
        "participant": [
            {
                "individual": {
                    "reference": "Practitioner/9"
                }
            }
        ],
        "serviceProvider": {
            "reference": "Organization/8",
            "display": "Kawempe National Referral Hospital"
        },
        "location": [
            {
                "location": {
                    "reference": "Location/10",
                    "display": "Eye Clinic"
                },
                "status": "active"
            }
        ]
    }

def create_observation_resource(obs, patient_id, encounter_id):
    return {
        "resourceType": "Observation",
        "id": generate_id(),
        "status": "final",
        "code": {
            "text": obs.get("type")
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "encounter": {
            "reference": f"Encounter/{encounter_id}"
        },
        "valueString": obs.get("value"),
        "effectiveDateTime": obs.get("date") or datetime.utcnow().isoformat()
    }

def create_medication_statement(med, patient_id, encounter_id):
    return {
        "resourceType": "MedicationStatement",
        "id": generate_id(),
        "status": "active",
        "medicationCodeableConcept": {
            "text": med.get("name")
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "context": {
            "reference": f"Encounter/{encounter_id}"
        },
        "effectivePeriod": {
            "start": med.get("start"),
            "end": med.get("end")
        },
        "dosage": [{
            "text": med.get("dosage")
        }]
    }


