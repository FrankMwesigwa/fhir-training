from flask import Flask, request, jsonify
import requests
from fhir_utils import (
    create_patient_resource, create_encounter_resource,
    create_observation_resource, create_medication_statement
)

app = Flask(__name__)

FHIR_SERVER_URL = "http://161.97.109.88:8080/fhir" 

@app.route('/api/fhir', methods=['POST'])
def receive_patient_bundle():
    try:
        data = request.get_json()

        patient_data = data.get("patient")
        encounter_data = data.get("encounter")
        observations = data.get("observations", [])
        medications = data.get("medications", [])

        patient_resource = create_patient_resource(patient_data)
        encounter_resource = create_encounter_resource(encounter_data, patient_resource["id"])

        bundle_entries = [
            {
                "resource": patient_resource,
                "request": {"method": "POST", "url": "Patient"}
            },
            {
                "resource": encounter_resource,
                "request": {"method": "POST", "url": "Encounter"}
            }
        ]

        for obs in observations:
            obs_resource = create_observation_resource(obs, patient_resource["id"], encounter_resource["id"])
            bundle_entries.append({
                "resource": obs_resource,
                "request": {"method": "POST", "url": "Observation"}
            })

        for med in medications:
            med_resource = create_medication_statement(med, patient_resource["id"], encounter_resource["id"])
            bundle_entries.append({
                "resource": med_resource,
                "request": {"method": "POST", "url": "MedicationStatement"}
            })
        

        bundle = {
            "resourceType": "Bundle",
            "type": "transaction",
            "entry": bundle_entries
        }

        fhir_response = requests.post(f"{FHIR_SERVER_URL}", json=bundle, headers={"Content-Type": "application/fhir+json"})
        return jsonify(fhir_response.json()), fhir_response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)