from api.conceptDictionary.concept_dictionary import ConceptDictionary


class MentalHealthExtractor:
    emr_concept_dictionary = ConceptDictionary()

    def extract_mental_health_field(self, chronic_lung_data):
        visit_details = chronic_lung_data['doc']['fields']['visit_details']
        visit_type = chronic_lung_data['doc']['fields']["visit_details"]['visit']
        visit_date = str(chronic_lung_data['doc']['fields']['visit_details']["visit_date"])

        mental_health_encounter = {
            "patient": "",
            "encounterType": "D51F45F8-0EEA-4231-A7E9-C45D57F1CBA1",
            "encounterDatetime": "2021-03-29",
            "location": "976dcd06-c40e-4e2e-a0de-35a54c7a52ef",
            "obs": [

            ]
        }

        if "visit_date" in visit_details:
            mental_health_encounter["encounterDatetime"] = \
                chronic_lung_data['doc']['fields']['visit_details']['visit_date']
        if "height" in visit_details:
            mental_health_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("height"),
                "value": visit_details['height']
            })
        if "weight" in visit_details:
            mental_health_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("weight"),
                "value": visit_details['weight']
            })
        if "next_appointment_date" in visit_details:
            mental_health_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("appointment_date"),
                "value": visit_details['next_appointment_date']
            })

        mental_health_visit_details = chronic_lung_data['doc']['fields']['mental_health_visit_details']
        if "ncd_side_effects" in mental_health_visit_details:
            side_effects = mental_health_visit_details["ncd_side_effects"]
            if side_effects == "yes":
                mental_health_encounter["obs"].append({
                    "concept": self.emr_concept_dictionary.get_concepts().get("ncd_side_effects"),
                    "value": True
                })
            if side_effects == "no":
                mental_health_encounter["obs"].append({
                    "concept": self.emr_concept_dictionary.get_concepts().get("ncd_side_effects"),
                    "value": False
                })
        if "mental_health_medication" in mental_health_visit_details:
            medication_list = str(mental_health_visit_details['mental_health_medication']).split()
            for each_medication in medication_list:
                mental_health_encounter["obs"].append({
                    "concept": self.emr_concept_dictionary.get_concepts().get("drug_set"),
                    "groupMembers": [
                        {
                            "concept": self.emr_concept_dictionary.get_concepts().get("drug_used"),
                            "value": self.emr_concept_dictionary.get_concepts().get(each_medication.lower())
                        }
                    ]
                })

        return mental_health_encounter
