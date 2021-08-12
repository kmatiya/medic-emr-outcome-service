from api.conceptDictionary.concept_dictionary import ConceptDictionary


class DiabetesHypertensionFieldExtractor:
    emr_concept_dictionary = ConceptDictionary()

    def extract_diabetes_hypertension_field(self, diabetes_hypertension_data):
        visit_details = diabetes_hypertension_data['doc']['fields']['visit_details']
        visit_type = diabetes_hypertension_data['doc']['fields']["visit_details"]['visit']
        visit_date = str(diabetes_hypertension_data['doc']['fields']['visit_details']["visit_date"])

        diabetes_hypertension_encounter = {
            "patient": "",
            "encounterType": "66079de4-a8df-11e5-bf7f-feff819cdc9f",
            "encounterDatetime": "2021-03-29",
            "location": "976dcd06-c40e-4e2e-a0de-35a54c7a52ef",
            "obs": [

            ]
        }

        if "visit_date" in visit_details:
            diabetes_hypertension_encounter["encounterDatetime"] = diabetes_hypertension_data['doc']['fields']['visit_details']['visit_date']
        if "height" in visit_details:
            diabetes_hypertension_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("height"),
                "value": visit_details['height']
            })
        if "weight" in visit_details:
            diabetes_hypertension_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("weight"),
                "value": visit_details['weight']
            })
        if "next_appointment_date" in visit_details:
            diabetes_hypertension_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("appointment_date"),
                "value": visit_details['next_appointment_date']
            })

        diabetes_bp_visit_details = diabetes_hypertension_data['doc']['fields']['diabetes_hypertension_visit_details']
        if "bp_systolic" in diabetes_bp_visit_details:
            tb_status_suspected = diabetes_bp_visit_details['bp_systolic']
            diabetes_hypertension_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("bp_systolic"),
                "value": diabetes_bp_visit_details['bp_systolic']
            })
        if "hba1c" in diabetes_bp_visit_details:
            diabetes_hypertension_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("hba1c"),
                "value": diabetes_bp_visit_details['hba1c']
            })

        if "blood_sugar" in diabetes_bp_visit_details:
            finger_stick = self.emr_concept_dictionary.get_concepts().get(str(diabetes_bp_visit_details['fingerstick']).lower())
            diabetes_hypertension_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("glucoseType"),
                "value": self.emr_concept_dictionary.get_concepts().get(str(diabetes_bp_visit_details['blood_sugar']).lower())
            })

        if "fingerstick" in diabetes_bp_visit_details:
            diabetes_hypertension_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("serumGlucose"),
                "value": diabetes_bp_visit_details['fingerstick']
            })
            
        if "diabetes_hypertension_medication" in diabetes_bp_visit_details:
            medication_list = str(diabetes_bp_visit_details['diabetes_hypertension_medication']).split()
            for each_medication in medication_list:
                diabetes_hypertension_encounter["obs"].append({
                    "concept": self.emr_concept_dictionary.get_concepts().get("drug_set"),
                    "groupMembers": [
                        {
                            "concept": self.emr_concept_dictionary.get_concepts().get("drug_used"),
                            "value": self.emr_concept_dictionary.get_concepts().get(each_medication.lower())
                        }
                    ]
                })
        return diabetes_hypertension_encounter
