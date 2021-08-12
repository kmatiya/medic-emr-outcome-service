from api.conceptDictionary.concept_dictionary import ConceptDictionary


class EpilepsyExtractor:
    emr_concept_dictionary = ConceptDictionary()

    def extract_epilepsy_field(self, chronic_lung_data):
        visit_details = chronic_lung_data['doc']['fields']['visit_details']
        visit_type = chronic_lung_data['doc']['fields']["visit_details"]['visit']
        visit_date = str(chronic_lung_data['doc']['fields']['visit_details']["visit_date"])

        epilepsy_encounter = {
            "patient": "",
            "encounterType": "1EEDD2F6-EF28-4409-8E8C-F4FEC0746E72",
            "encounterDatetime": "2021-03-29",
            "location": "976dcd06-c40e-4e2e-a0de-35a54c7a52ef",
            "obs": [

            ]
        }

        if "visit_date" in visit_details:
            epilepsy_encounter["encounterDatetime"] = \
                chronic_lung_data['doc']['fields']['visit_details']['visit_date']
        if "height" in visit_details:
            epilepsy_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("height"),
                "value": visit_details['height']
            })
        if "weight" in visit_details:
            epilepsy_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("weight"),
                "value": visit_details['weight']
            })
        if "next_appointment_date" in visit_details:
            epilepsy_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("appointment_date"),
                "value": visit_details['next_appointment_date']
            })

        epilepsy_visit_details = chronic_lung_data['doc']['fields']['epilepsy_visit_details']
        if "seizure_no" in epilepsy_visit_details:
            epilepsy_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("seizure_no"),
                "value": epilepsy_visit_details['seizure_no']
            })
        if "epilepsy_medication" in epilepsy_visit_details:
            medication_list = str(epilepsy_visit_details['epilepsy_medication']).split()
            for each_medication in medication_list:
                epilepsy_encounter["obs"].append({
                    "concept": self.emr_concept_dictionary.get_concepts().get("drug_set"),
                    "groupMembers": [
                        {
                            "concept": self.emr_concept_dictionary.get_concepts().get("drug_used"),
                            "value": self.emr_concept_dictionary.get_concepts().get(each_medication.lower())
                        }
                    ]
                })

        return epilepsy_encounter
