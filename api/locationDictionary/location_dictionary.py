class LocationDictionary:
    __location_list = {
        "neno_district_hospital": "0d414ce2-5ab4-11e0-870c-9f6107fee88e",
        "dambe_clinic": "976dcd06-c40e-4e2e-a0de-35a54c7a52ef",
        "binje_outreach_clinic": "3093e2ab-0eee-4bc2-aacf-8d51d77c7698",
        "golden_outreach_clinic": "6c090943-f5a3-47ed-b16a-b69cc5750a49",
        "ligowe_hc": "0d417e38-5ab4-11e0-870c-9f6107fee88e",
        "luwani_rhc": "0d416506-5ab4-11e0-870c-9f6107fee88e",
        "magaleta_hc": "0d414eae-5ab4-11e0-870c-9f6107fee88e",
        "matandani_rural_health_center": "0d415200-5ab4-11e0-870c-9f6107fee88e",
        "neno_mission_hc": "0d41505c-5ab4-11e0-870c-9f6107fee88e",
        "nsambe_hc": "0d416830-5ab4-11e0-870c-9f6107fee88e",
        "ntaja_outreach_clinic": "22e76417-b6d9-41a2-84ee-bb07175d2ddf"
    }

    def get_locations(self):
        return self.__location_list

    def get_location_uuid_by_key(self, key):
        return self.__location_list.get(key)
