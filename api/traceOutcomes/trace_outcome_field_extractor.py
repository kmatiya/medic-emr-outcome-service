from api.conceptDictionary.concept_dictionary import ConceptDictionary


class TraceOutcomesFieldExtractor:
    emr_concept_dictionary = ConceptDictionary()

    def extract_trace_outcomes_field(self, trace_outcome_data):
        trace_details = trace_outcome_data['doc']['fields']['trace_details']

        trace_followup_encounter = {
            "patient": "212ee675-70c9-4962-83c1-74fedec8c867",
            "encounterType": "563ACC45-E3CE-4930-8F34-4F41CB35017F",
            "encounterDatetime": "2021-03-01",
            "location": "",
            "obs": [

            ]
        }
    #    if "appt_date" in trace_outcome_data['doc']['fields']:
    #        trace_followup_encounter["encounterDatetime"] = trace_outcome_data['doc']['fields']['appt_date']
        if "trace_reasons" in trace_outcome_data['doc']['fields']:
            trace_followup_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("reason_for_missing_appt"),
                "value": str(trace_outcome_data['doc']['fields']['trace_reasons'])
            })
        if "patient_found" in trace_details:
            trace_followup_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("patient_found"),
                "value": self.emr_concept_dictionary.get_concepts().get(trace_details['patient_found'])
            })
        if "health_complaints" in trace_details:
            trace_followup_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("health_complaints"),
                "value": str(trace_details['health_complaints'])
            })

        if "social_complaints" in trace_details:
            trace_followup_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("social_complaints"),
                "value": str(trace_details['social_complaints'])
            })

        if "agreed_to_return" in trace_details:
            trace_followup_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("agreed_to_return"),
                "value": self.emr_concept_dictionary.get_concepts().get(trace_details['agreed_to_return'])
            })

        if "date_given" in trace_details:
            trace_followup_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("date_given"),
                "value": str(trace_details['date_given'])
            })

        if "patient_behavior" in trace_details:
            trace_followup_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("patient_behavior"),
                "value": self.emr_concept_dictionary.get_concepts().get(str(trace_details['patient_behavior']).lower())
            })

        '''if "remarks" in trace_details:
            trace_followup_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("remarks"),
                "value": str(trace_details['remarks'])
            })'''

        if "next_attempt_date" in trace_details:
            trace_followup_encounter["obs"].append({
                "concept": self.emr_concept_dictionary.get_concepts().get("next_attempt_date"),
                "value": str(trace_details['next_attempt_date'])
            })
        return trace_followup_encounter
