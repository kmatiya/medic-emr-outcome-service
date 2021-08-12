from api.conceptDictionary.concept_dictionary import ConceptDictionary


class ChronicLungDiseaseExtractor:
    emr_concept_dictionary = ConceptDictionary()

    def extract_chronic_lung_field(self, chronic_lung_data):
        visit_details = chronic_lung_data['doc']['fields']['visit_details']
        visit_type = chronic_lung_data['doc']['fields']["visit_details"]['visit']
        visit_date = str(chronic_lung_data['doc']['fields']['visit_details']["visit_date"])

        chronic_lung_encounter = {
            "patient": "",
            "encounterType": "f4596df5-925c-11e5-a1de-e82aea237783",
            "encounterDatetime": "2021-03-29",
            "location": "976dcd06-c40e-4e2e-a0de-35a54c7a52ef",
            "obs": [

            ]
        }

        if "visit_date" in visit_details:
            chronic_lung_encounter["encounterDatetime"] = \
                chronic_lung_data['doc']['fields']['visit_details']['visit_date']
        if "height" in visit_details:
            chronic_lung_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("height"),
                "value": visit_details['height']
            })
        if "weight" in visit_details:
            chronic_lung_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("weight"),
                "value": visit_details['weight']
            })
        if "next_appointment_date" in visit_details:
            chronic_lung_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("appointment_date"),
                "value": visit_details['next_appointment_date']
            })

        chronic_lung_visit_details = chronic_lung_data['doc']['fields']['chronic_lung_disease_visit_details']
        if "exacerbation_today" in chronic_lung_visit_details:
            chronic_lung_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("exacerbation_today"),
                "value": self.emr_concept_dictionary.get_concepts().get(chronic_lung_visit_details['exacerbation_today'])
            })
        if "asthma_severity" in chronic_lung_visit_details:
            chronic_lung_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("asthma_severity"),
                "value": self.emr_concept_dictionary.get_concepts().get(chronic_lung_visit_details['asthma_severity'])
            })

        if "copd" in chronic_lung_visit_details:
            if chronic_lung_visit_details['copd'] == "yes":
                chronic_lung_encounter["obs"].append({
                    "concept": self.emr_concept_dictionary.get_concepts().get("chronic_care_diagnosis"),
                    "value": self.emr_concept_dictionary.get_concepts().get("copd")
                })
        return chronic_lung_encounter
