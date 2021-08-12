from api.conceptDictionary.concept_dictionary import ConceptDictionary


class ArtFieldExtractor:
    emr_concept_dictionary = ConceptDictionary()

    def extract_art_field(self, art_data):
        visit_details = art_data['doc']['fields']['visit_details']
        visit_type = art_data['doc']['fields']["visit_details"]['visit']
        visit_date = str(art_data['doc']['fields']['visit_details']["visit_date"])

        art_encounter = {
            "patient": "",
            "encounterType": "664b8650-977f-11e1-8993-905e29aff6c1",
            "encounterDatetime": "2021-03-29",
            "location": "976dcd06-c40e-4e2e-a0de-35a54c7a52ef",
            "obs": [

            ]
        }
        if "visit_date" in visit_details:
            art_encounter["encounterDatetime"] = art_data['doc']['fields']['visit_details']['visit_date']
        if "height" in visit_details:
            art_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("height"),
                "value": visit_details['height']
            })
        if "weight" in visit_details:
            art_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("weight"),
                "value": visit_details['weight']
            })
        if "next_appointment_date" in visit_details:
            art_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("appointment_date"),
                "value": visit_details['next_appointment_date']
            })

        if str(visit_type).__contains__("art"):
            art_visit_details = art_data['doc']['fields']["art_visit_details"]
            if "pregnancy_care" in art_visit_details:
                art_encounter["obs"].append({
                    "concept": self.emr_concept_dictionary.get_concepts().get("pregnant/lactating"),
                    "value": self.emr_concept_dictionary.get_concepts().get(str(art_visit_details['pregnancy_care']).lower())
                })

            if "tb_status" in art_visit_details:
                tb_status_suspected = art_visit_details['tb_status']
                if str(tb_status_suspected).lower() == "yes":
                    tb_status_suspected = self.emr_concept_dictionary.get_concepts().get("tb_suspected")
                else:
                    tb_status_suspected = self.emr_concept_dictionary.get_concepts().get("tb_not_suspected")

                art_encounter["obs"].append({
                    "concept": self.emr_concept_dictionary.get_concepts().get("tb_status"),
                    "value": tb_status_suspected
                })
            if "pill_count" in art_visit_details:
                art_encounter["obs"].append({
                    "concept": self.emr_concept_dictionary.get_concepts().get("pill_count"),
                    "value": art_visit_details['pill_count']
                })
            if "doses_missed" in art_visit_details:
                art_encounter["obs"].append({
                    "concept": self.emr_concept_dictionary.get_concepts().get("doses_missed"),
                    "value": art_visit_details['doses_missed']
                })

            if "regimen" in art_visit_details:
                art_encounter["obs"].append({
                    "concept": self.emr_concept_dictionary.get_concepts().get("regimen"),
                    "value": self.emr_concept_dictionary.get_concepts().get(art_visit_details["regimen"])
                })
            if "arvs_no" in art_visit_details:
                art_encounter["obs"].append({
                    "concept": self.emr_concept_dictionary.get_concepts().get("arvs_no"),
                    "value": art_visit_details['arvs_no']
                })
            if "arvs_issuee" in art_visit_details:
                issued_to = art_visit_details["arvs_issuee"]
                if str(issued_to).lower() == "patient":
                    issued_to = True
                else:
                    issued_to = False
                art_encounter["obs"].append({
                    "concept": self.emr_concept_dictionary.get_concepts().get("arvs_given_to"),
                    "value": issued_to
                })
            if "art_side_effects" in art_visit_details:
                side_effects = str(art_visit_details['art_side_effects']).split()
                for each_side_effect in side_effects:
                    art_encounter["obs"].append({
                        "concept": self.emr_concept_dictionary.get_concepts().get("cpt_ipt_group"),
                        "groupMembers": [
                            {
                                "concept": self.emr_concept_dictionary.get_concepts().get("cpt_ipt"),
                                "value": self.emr_concept_dictionary.get_concepts().get(each_side_effect.lower())
                            },
                            {
                                "concept": self.emr_concept_dictionary.get_concepts().get("cpt_ipt_pills"),
                                "value": visit_details["cpt_ipt_pills"]
                            }
                        ]
                    })
        return art_encounter
