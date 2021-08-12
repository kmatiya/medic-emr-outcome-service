class EncounterDictionary:
    __encounter_list = {
        "art_followup": "664b8650-977f-11e1-8993-905e29aff6c1",
        "chronic_lung_followup": "f4596df5-925c-11e5-a1de-e82aea237783",
        "diabetes_hypertension_followup": "66079de4-a8df-11e5-bf7f-feff819cdc9f",
        "epilepsy_followup": "1EEDD2F6-EF28-4409-8E8C-F4FEC0746E72",
        "mental_health_followup": "D51F45F8-0EEA-4231-A7E9-C45D57F1CBA1",
        "trace_followup": "563ACC45-E3CE-4930-8F34-4F41CB35017F",
        "viral_load": "9959A261-2122-4AE1-A89D-1CA444B712EA",
        "trace_initial": "7EBBEBD8-CF07-489B-B88D-CEBA274C66D5"
    }

    def get_encounters(self):
        return self.__encounter_list

    def get_encounter_uuid_by_key(self, key):
        return self.__encounter_list.get(key)
