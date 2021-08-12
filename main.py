import json

import requests
from requests.auth import HTTPBasicAuth
from datetime import date
import datetime
import time
import logging

from api.encounterDictionary.encounter_dictionary import EncounterDictionary
from api.locationDictionary.location_dictionary import LocationDictionary
from api.traceOutcomes.trace_outcome_field_extractor import TraceOutcomesFieldExtractor
from api.visitVerification.art_field_extractor import ArtFieldExtractor
from api.visitVerification.chronic_lung_field_extractor import ChronicLungDiseaseExtractor
from api.visitVerification.diabetes_hypertension_field_extractor import DiabetesHypertensionFieldExtractor
from api.visitVerification.epilepsy_field_extractor import EpilepsyExtractor
from api.visitVerification.mental_field_extractor import MentalHealthExtractor

backup = '1618371836266'
medic_mobile_username = "openmrs"
medic_mobile_pwd = "S3cr3t_1"

encounter_url = "http://localhost:8080/openmrs/ws/rest/v1/encounter"
patient_url = "http://localhost:8080/openmrs/ws/rest/v1/patient"
emr_username = "openmrs"
emr_pwd = "openmrs"


def get_emr_patient(url, param, username, password):
    return requests.get(url, params=param,
                        auth=HTTPBasicAuth(username=username,
                                           password=password))


def get_emr_uuid(response):
    patient = json.loads(response.text)
    if len(patient["results"]) == 0:
        return ""
    return patient["results"][0]["uuid"]


def check_encounter_exist(encounter_response):
    encounter = json.loads(encounter_response.text)
    if len(encounter["results"]) == 0:
        return False
    return True


if __name__ == '__main__':
    print(date.today())
    print(date.today() + datetime.timedelta(days=1))
    today = datetime.timedelta(8)
    seven_days = date.today() - today
    print(seven_days)
    dt = datetime.datetime.combine(seven_days, datetime.datetime.min.time())
    print(dt)
    end_timestamp = int(round(time.time() * 1000))
    start_timestamp = int(round(dt.timestamp() * 1000))
    print("timestamp")
    print(start_timestamp)
    print(end_timestamp)
    medic_mobile_visit_verification_url = 'https://pih-malawi.dev.medicmobile.org/medic/_design/medic-client/_view' \
                                          '/yendanafe_omrs?startkey=[' \
                                          '%22visit_verification%22,' + str(start_timestamp) + ']&endkey=[' \
                                                                                               '%22visit_verification%22,' \
                                          + str(end_timestamp) + ']&include_docs=true'

    medic_mobile_trace_followup_url = 'https://pih-malawi.dev.medicmobile.org/medic/_design/medic-client/_view' \
                                      '/yendanafe_omrs?startkey=[%22trace_follow_up%22,' + str(start_timestamp) + \
                                      ']&endkey=[' \
                                      '%22trace_follow_up%22,' + str(end_timestamp) + ']&include_docs=true'

    log_file = "log_" + str(datetime.datetime.now())
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filename='logs/' + log_file,
                        filemode='w')

    logging.info("***************************************************************************************************")
    logging.info("Running Process for visit verification and patient trace outcomes today:" + str(date.today()))
    encounter_dictionary = EncounterDictionary()
    location_dictionary = LocationDictionary()
    try:
        logging.info("Get Visit verification data")
        get_result = requests.get(medic_mobile_visit_verification_url,
                                  auth=HTTPBasicAuth(username=medic_mobile_username, password=medic_mobile_pwd))
        logging.info("Verification response: status code: " + str(get_result.status_code) + ". Response:" +
                     str(get_result.text))
        rows = json.loads(get_result.text)
        logging.info(rows)
        if get_result.status_code == 200:
            data = rows['rows']
            logging.info("Verification Data:" + str(data))
            logging.info("Looping through each object")
            for each in data:
                visit_type = str(each['doc']['fields']["visit_details"]['visit']).lower()
                visit_location = str(each['doc']['fields']["visit_details"]['facility_name']).lower()
                visit_date = str(each['doc']['fields']["visit_details"]['visit_date'])
                # test = datetime.datetime.strptime(each['doc']['fields']["visit_details"]['visit_date'], "%Y-%m-%d").strftime("%Y-%m-%d")
                end_date = datetime.datetime.strptime(each['doc']['fields']["visit_details"]['visit_date'],
                                                      "%Y-%m-%d")
                end_date += datetime.timedelta(days=1)
                end_date = end_date.date()
                # end_date = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").strftime("%Y-%m-%d")

                encounter_par = {
                    'patient': "",
                    'fromdate': each['doc']['fields']["visit_details"]['visit_date'],
                    'todate': end_date,
                    'encounterType': ""
                }
                params = {
                    "q": each['doc']['fields']['patient_uuid'],
                    "v": "default",
                    "limit": "1"
                }
                '''params = {
                    "q": "a7f760aa-458c-44c6-bff7-837e5daf92e71",
                    "v": "default",
                    "limit": "1"
                }'''
                patient_response = get_emr_patient(patient_url, params, emr_username, emr_pwd)
                logging.info("Get patient from EMR result: status code: " + str(patient_response.status_code)
                             + ". response: " + patient_response.text)
                try:
                    if visit_type.lower().__contains__("art") and patient_response.status_code == 200:
                        print("ART visit")
                        patient_uuid = get_emr_uuid(patient_response)
                        encounter_par["encounterType"] = encounter_dictionary.get_encounter_uuid_by_key("art_followup")
                        encounter_par["patient"] = patient_uuid
                        logging.info("ART_FOLLOWUP Encounter object to check from EMR" + str(encounter_par))
                        encounter_result = requests.get(encounter_url, params=encounter_par,
                                                        auth=HTTPBasicAuth(username=emr_username, password=emr_pwd))
                        logging.info("Check encounter exist from emr response: status code: "
                                     + str(encounter_result.status_code) + ". response: " + encounter_result.text)
                        encounter_exist = check_encounter_exist(encounter_result)
                        if patient_uuid != "" and encounter_exist is False:
                            art_extractor = ArtFieldExtractor()
                            extract_payload = art_extractor.extract_art_field(each)
                            extract_payload["location"] = location_dictionary.get_location_uuid_by_key(visit_location)
                            extract_payload["encounterDatetime"] = visit_date
                            print(extract_payload)
                            logging.info("Patient ART Visit: " + str(extract_payload))
                            post_result = requests.post(encounter_url, json=extract_payload,
                                                        auth=HTTPBasicAuth(username=emr_username, password=emr_pwd))
                            logging.info("Post to EMR result:" + post_result.text)

                    if visit_type.__contains__("ncd") and str(
                            each['doc']['fields']["visit_details"]['ncds']).__contains__("diabetes_hypertension"):
                        print("Diabetes visit")
                        patient_uuid = get_emr_uuid(patient_response)
                        encounter_par["encounterType"] = encounter_dictionary.get_encounter_uuid_by_key(
                            "diabetes_hypertension_followup")
                        encounter_par["patient"] = patient_uuid
                        logging.info(
                            "DIABETES_HYPERTENSION_FOLLOWUP Encounter object to check from EMR" + str(encounter_par))
                        encounter_result = requests.get(encounter_url, params=encounter_par,
                                                        auth=HTTPBasicAuth(username=emr_username, password=emr_pwd))
                        logging.info("Check encounter exist from emr response: status code: "
                                     + str(encounter_result.status_code) + ". response: " + encounter_result.text)
                        encounter_exist = check_encounter_exist(encounter_result)
                        if patient_uuid != "" and encounter_exist is False:
                            diabetes_hypertension_extractor = DiabetesHypertensionFieldExtractor()
                            extract_payload = diabetes_hypertension_extractor.extract_diabetes_hypertension_field(each)
                            print(extract_payload)
                            extract_payload["location"] = location_dictionary.get_location_uuid_by_key(visit_location)
                            extract_payload["encounterDatetime"] = visit_date
                            logging.info("Patient DIABETES HYPERTENSION VISIT: " + str(extract_payload))
                            post_result = requests.post(encounter_url, json=extract_payload,
                                                        auth=HTTPBasicAuth(username=emr_username, password=emr_pwd))
                            logging.info("Post to EMR result: status code: " + str(post_result.status_code)
                                         + ".Response: " + post_result.text)
                    if visit_type.__contains__("ncd") and str(
                            each['doc']['fields']["visit_details"]['ncds']).__contains__("chronic_lung_disease"):
                        print("Chronic Lung visit")
                        patient_uuid = get_emr_uuid(patient_response)
                        encounter_par["encounterType"] = encounter_dictionary.get_encounter_uuid_by_key(
                            "chronic_lung_followup")
                        encounter_par["patient"] = patient_uuid
                        logging.info(
                            "CHRONIC_LUNG_FOLLOWUP Encounter object to check from EMR" + str(encounter_par))
                        encounter_result = requests.get(encounter_url, params=encounter_par,
                                                        auth=HTTPBasicAuth(username=emr_username, password=emr_pwd))
                        logging.info("Check encounter exist from emr response: status code: "
                                     + str(encounter_result.status_code) + ". response: " + encounter_result.text)
                        encounter_exist = check_encounter_exist(encounter_result)
                        if patient_uuid != "" and encounter_exist is False:
                            chronic_lung_extractor = ChronicLungDiseaseExtractor()
                            extract_payload = chronic_lung_extractor.extract_chronic_lung_field(each)
                            print(extract_payload)
                            extract_payload["location"] = location_dictionary.get_location_uuid_by_key(visit_location)
                            extract_payload["encounterDatetime"] = visit_date
                            logging.info("Patient CHRONIC LUNG VISIT: " + str(extract_payload))
                            post_result = requests.post(encounter_url, json=extract_payload,
                                                        auth=HTTPBasicAuth(username=emr_username, password=emr_pwd))
                            print(post_result.text)
                            logging.info("Post to EMR result: status code: " + str(post_result.status_code)
                                         + ".Response: " + post_result.text)
                    if visit_type.__contains__("ncd") and str(
                            each['doc']['fields']["visit_details"]['ncds']).__contains__("epilepsy"):
                        print("Epilepsy visit")
                        patient_uuid = get_emr_uuid(patient_response)
                        encounter_par["encounterType"] = encounter_dictionary.get_encounter_uuid_by_key(
                            "epilepsy_followup")
                        encounter_par["patient"] = patient_uuid
                        logging.info(
                            "EPILEPSY_FOLLOWUP Encounter object to check from EMR" + str(encounter_par))
                        encounter_result = requests.get(encounter_url, params=encounter_par,
                                                        auth=HTTPBasicAuth(username=emr_username, password=emr_pwd))
                        logging.info("Check encounter exist from emr response: status code: "
                                     + str(encounter_result.status_code) + ". response: " + encounter_result.text)
                        encounter_exist = check_encounter_exist(encounter_result)
                        if patient_uuid != "" and encounter_exist is False:
                            epilepsy_extractor = EpilepsyExtractor()
                            extract_payload = epilepsy_extractor.extract_epilepsy_field(each)
                            print(extract_payload)
                            extract_payload["location"] = location_dictionary.get_location_uuid_by_key(visit_location)
                            extract_payload["encounterDatetime"] = visit_date
                            logging.info("Patient EPILEPSY VISIT: " + str(extract_payload))
                            post_result = requests.post(encounter_url, json=extract_payload,
                                                        auth=HTTPBasicAuth(username=emr_username, password=emr_pwd))
                            print(post_result.text)
                            logging.info("Post to EMR result: status code: " + str(post_result.status_code)
                                         + ".Response: " + post_result.text)
                    if visit_type.__contains__("ncd") and str(
                            each['doc']['fields']["visit_details"]['ncds']).__contains__("mental_health"):
                        print("Mental Health visit")
                        patient_uuid = get_emr_uuid(patient_response)
                        encounter_par["encounterType"] = encounter_dictionary.get_encounter_uuid_by_key(
                            "mental_health_followup")
                        encounter_par["patient"] = patient_uuid
                        logging.info(
                            "MENTAL_HEALTH_FOLLOWUP Encounter object to check from EMR" + str(encounter_par))
                        encounter_result = requests.get(encounter_url, params=encounter_par,
                                                        auth=HTTPBasicAuth(username=emr_username, password=emr_pwd))
                        logging.info("Check encounter exist from emr response: status code: "
                                     + str(encounter_result.status_code) + ". response: " + encounter_result.text)
                        encounter_exist = check_encounter_exist(encounter_result)
                        if patient_uuid != "" and encounter_exist is False:
                            mental_health_extractor = MentalHealthExtractor()
                            extract_payload = mental_health_extractor.extract_mental_health_field(each)
                            print(extract_payload)
                            extract_payload["location"] = location_dictionary.get_location_uuid_by_key(visit_location)
                            extract_payload["encounterDatetime"] = visit_date
                            logging.info("Patient MENTAL HEALTH VISIT: " + str(extract_payload))
                            post_result = requests.post(encounter_url, json=extract_payload,
                                                        auth=HTTPBasicAuth(username=emr_username, password=emr_pwd))
                            print(post_result.text)
                            logging.info("Check encounter exist from emr response: status code: "
                                         + str(encounter_result.status_code) + ". response: " + encounter_result.text)

                except Exception as e:
                    print("Error with visit data:" + str(each))
                    logging.info("Error with visit data:" + str(each))
                    logging.error(e)
    except Exception as e:
        logging.error(e)
    try:
        logging.info("Get Trace Outcomes Data")
        get_trace_followup_result = requests.get(medic_mobile_trace_followup_url,
                                                 auth=HTTPBasicAuth(username=medic_mobile_username,
                                                                    password=medic_mobile_pwd))
        logging.info("Trace Outcomes response: status code: " + str(get_trace_followup_result.status_code)
                     + ". Response:" + str(get_trace_followup_result.text))
        trace_follow_up_data = json.loads(get_trace_followup_result.text)
        if get_trace_followup_result.status_code == 200:
            trace_follow_up_data = trace_follow_up_data['rows']
            logging.info("Outcomes Data: " + str(trace_follow_up_data))
            for each in trace_follow_up_data:
                try:
                    complete_patient_url = patient_url
                    params = {
                        "q": each['doc']['fields']['patient_uuid'],
                        "v": "default",
                        "limit": "1"
                    }
                    '''params = {
                        "q": "a7f760aa-458c-44c6-bff7-837e5daf92e72",
                        "v": "default",
                        "limit": "1"
                    }'''
                    emr_patient_request = requests.get(patient_url, params=params,
                                                       auth=HTTPBasicAuth(username=emr_username,
                                                                          password=emr_pwd))
                    logging.info("Get patient from EMR result: status code: " + str(emr_patient_request.status_code)
                                 + ". response: " + emr_patient_request.text)
                    emr_patient = json.loads(emr_patient_request.text)
                    len_of_result = len(emr_patient['results'])

                    if emr_patient_request.status_code == 200 and 'trace_details' in str(
                            each['doc']['fields']) and get_emr_uuid(emr_patient_request) != "":
                        patient_uuid = get_emr_uuid(emr_patient_request)
                        start_date = date.today()
                        trace_details = each['doc']['fields']['trace_details']
                        trace_location = location_dictionary.get_location_uuid_by_key(
                            str(trace_details["facility_name"]))
                        trace_follow_up_extractor = TraceOutcomesFieldExtractor()
                        extract_payload = trace_follow_up_extractor.extract_trace_outcomes_field(each)
                        print(extract_payload)
                        logging.info("Patient Trace Outcome payload: " + str(extract_payload))
                        extract_payload["location"] = trace_location
                        # Check Trace initial visit exist

                        encounter_par = {
                            'patient': patient_uuid,
                            'fromdate': "2021-01-01",
                            'todate': date.today(),
                            'encounterType': encounter_dictionary.get_encounter_uuid_by_key("trace_initial")
                        }
                        encounter_result = requests.get(encounter_url, params=encounter_par,
                                                        auth=HTTPBasicAuth(username=emr_username, password=emr_pwd))
                        logging.info("Check encounter exist from emr response: status code: "
                                     + str(encounter_result.status_code) + ". response: " + encounter_result.text)
                        encounter_exist = check_encounter_exist(encounter_result)
                        if encounter_exist is True:
                            post_result = requests.post(encounter_url, json=extract_payload,
                                                        auth=HTTPBasicAuth(username=emr_username, password=emr_pwd))
                            print(post_result.status_code)
                            print(post_result.text)
                            logging.info("Post to EMR result: status code: " + str(post_result.status_code)
                                         + ".Response: " + post_result.text)
                        else:
                            trace_initial_encounter = {
                                "patient": patient_uuid,
                                "encounterType": encounter_dictionary.get_encounter_uuid_by_key("trace_initial"),
                                "encounterDatetime": str(start_date),
                                "location": trace_location,
                            }
                            logging.info("Creating Trace Initial encounter. Payload: " + str(trace_initial_encounter))
                            post_trace_initial_result = requests.post(encounter_url, json=trace_initial_encounter,
                                                                      auth=HTTPBasicAuth(username=emr_username,
                                                                                         password=emr_pwd))
                            logging.info(
                                "Post to EMR result: status code: " + str(post_trace_initial_result.status_code)
                                + ".Response: " + post_trace_initial_result.text)
                            post_result = requests.post(encounter_url, json=extract_payload,
                                                        auth=HTTPBasicAuth(username=emr_username, password=emr_pwd))
                            print(post_result.status_code)
                            print(post_result.text)
                            logging.info("Post to EMR result: status code: " + str(post_result.status_code)
                                         + ".Response: " + post_result.text)

                    else:
                        print("Outcome Not Added: " + str(each))
                        logging.info("Outcome Not Added: " + str(each))
                except Exception as e:
                    print("Error with visit data:" + str(each))
                    print(e)
                    logging.info("Error with Trace Outcome data:" + str(each))
                    logging.error(e)
    except Exception as e:
        print(e)
        logging.error(e)
