class workflowDictionary:
    __workflow_state_list = {
        #Hiv State List
        "hiv_patient_defaulted": "6687fff4-977f-11e1-8993-905e29aff6c1",
        "hiv_z_deprecated_patient_transferred_in": "66885396-977f-11e1-8993-905e29aff6c1",
        "hiv_on_antiretrovirals": "6687fa7c-977f-11e1-8993-905e29aff6c1",
        "hiv_treatment_stopped": "6687f96e-977f-11e1-8993-905e29aff6c1",
        "hiv_patient_died": "6687f630-977f-11e1-8993-905e29aff6c1",
        "hiv_exposed_child": "668847a2-977f-11e1-8993-905e29aff6c1",
        "hiv_patient_tranferred_out": "6687f50e-977f-11e1-8993-905e29aff6c1",
        "hiv_patient_transferred_internally": "66882a88-977f-11e1-8993-905e29aff6c1",
        "hiv_discharged_uninfected": "668846d0-977f-11e1-8993-905e29aff6c1",
        "hiv_pre_art": "6687f284-977f-11e1-8993-905e29aff6c1",
        "hiv_z_deprecated_treatment_never_started_patient_refused": "6687fb94-977f-11e1-8993-905e29aff6c1",

        #Mental Health State List
        "mental_patient_defaulted": "19CEF51A-0823-4876-A8AF-7285B7077494",
        "mental_on_treatment": "5925718D-EA5E-43EB-9AE2-1CB342D8E318",
        "mental_in_advanced_care": "E0381FF3-2976-41F0-B853-28E842400E84",
        "mental_discharged": "42ACC789-C2BB-4EAA-8AC2-0BE7D0F5D4E8",
        "mental_patient_died": "D79B02C2-B473-47F1-A51C-6D40B2242B9C",
        "mental_treatment_stopped": "9F6F188C-42AB-45D8-BC8B-DBE78948072D",
        "mental_patient_transferred_out": "41AF39C1-7CE6-47E0-9BA7-9FD7C0354C12",

        #NCD State List
        "ncd_patient_defaulted": "3a4eb919-b942-4c9c-ba0e-defcebe5cd4b",
        "ncd_patient_transferred_out": "6688275e-977f-11e1-8993-905e29aff6c1",
        "ncd_in_advanced_care": "7c4d2e56-c8c2-11e8-9bc6-0242ac110001",
        "ncd_patient_died": "6688286c-977f-11e1-8993-905e29aff6c1",
        "ncd_on_treatment": "66882650-977f-11e1-8993-905e29aff6c1",
        "ncd_discharged": "6688297a-977f-11e1-8993-905e29aff6c1",
        "ncd_treatment_stopped": "dbe76d47-dbc4-4608-a578-97b6b62d9f63",

    }

    def get_workflow_states(self):
        return self.__workflow_state_list

    def get_workflow_state_uuid_by_key(self, key):
        return self.__workflow_state_list.get(key)
