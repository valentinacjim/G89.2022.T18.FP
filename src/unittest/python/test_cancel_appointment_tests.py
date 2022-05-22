"""Tests for cancel_appointment method"""
from unittest import TestCase
import os
import shutil
from freezegun import freeze_time
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_RF2_PATH, JSON_FILES_RF3_PATH
from uc3m_care import PatientsJsonStore
from uc3m_care import CancelAppointmentJsonStore


param_list_nok = [("duplication1.json", "JSON Decode Error - Wrong JSON Format"),
                  ("deletion1.json", "JSON Decode Error - Wrong JSON Format"),
                  ("duplication2.json", "JSON Decode Error - Wrong JSON Format"),
                  ("deletion2.json", "JSON Decode Error - Wrong JSON Format"),
                  ("duplication3.json", "JSON Decode Error - Wrong JSON Format"),
                  ("deletion3.json", "Bad label date signature"),
                  ("duplication4.json", "JSON Decode Error - Wrong JSON Format"),
                  ("deletion4.json", "JSON Decode Error - Wrong JSON Format"),
                  ("duplication6.json", "JSON Decode Error - Wrong JSON Format"),
                  ("deletion6.json", "JSON Decode Error - Wrong JSON Format"),
                  ("duplication7.json", "JSON Decode Error - Wrong JSON Format"),
                  ("deletion7.json", "JSON Decode Error - Wrong JSON Format"),
                  ("duplication8.json", "JSON Decode Error - Wrong JSON Format"),
                  ("deletion8.json", "JSON Decode Error - Wrong JSON Format"),
                  ("duplication10.json", "JSON Decode Error - Wrong JSON Format"),
                  ("deletion10.json", "JSON Decode Error - Wrong JSON Format"),
                  ("duplication12.json", "JSON Decode Error - Wrong JSON Format"),
                  ("deletion12.json", "JSON Decode Error - Wrong JSON Format"),
                  ("duplication13.json", "JSON Decode Error - Wrong JSON Format"),
                  ("deletion13.json", "JSON Decode Error - Wrong JSON Format"),
                  ("duplication14.json", "JSON Decode Error - Wrong JSON Format"),
                  ("deletion14.json", "JSON Decode Error - Wrong JSON Format"),
                  ("duplication16.json", "JSON Decode Error - Wrong JSON Format"),
                  ("deletion16.json", "JSON Decode Error - Wrong JSON Format"),
                  ("duplication18.json", "JSON Decode Error - Wrong JSON Format"),
                  ("deletion18.json", "JSON Decode Error - Wrong JSON Format"),
                  ("duplication20.json", "JSON Decode Error - Wrong JSON Format"),
                  ("deletion20.json", "JSON Decode Error - Wrong JSON Format"),
                  ("duplication22.json", "JSON Decode Error - Wrong JSON Format"),
                  ("deletion22.json", "JSON Decode Error - Wrong JSON Format"),
                  ("duplication23.json", "JSON Decode Error - Wrong JSON Format"),
                  ("deletion23.json", "JSON Decode Error - Wrong JSON Format"),
                  ("duplication24.json", "Bad label date signature"),
                  ("deletion24.json", "Bad label date signature"),
                  ("duplication25.json", "JSON Decode Error - Wrong JSON Format"),
                  ("deletion25.json", "JSON Decode Error - Wrong JSON Format"),
                  ("duplication28.json", "date_signature format is not valid"),
                  ("deletion28.json", "date_signature format is not valid"),
                  ("duplication31.json", "Bad label cancelation type"),
                  ("deletion31.json", "Bad label cancelation type"),
                  ("duplication35.json", "cancelation type format not valid"),
                  ("deletion35.json", "cancelation type format not valid"),
                  ("duplication38.json", "Bad label reason"),
                  ("deletion38.json", "Bad label reason"),
                  ("duplication42.json", "the reason is not valid"),
                  ("deletion42.json", "the reason is not valid"),
                  ("modification5.json", "JSON Decode Error - Wrong JSON Format"),
                  ("modification11.json", "JSON Decode Error - Wrong JSON Format"),
                  ("modification15.json", "JSON Decode Error - Wrong JSON Format"),
                  ("modification26.json", "JSON Decode Error - Wrong JSON Format"),
                  ("modification44.json", "JSON Decode Error - Wrong JSON Format"),
                  ("modification45.json", "Bad label date signature"),
                  ("modification48.json", "date_signature format is not valid"),
                  ("modification51.json", "Bad label cancelation type"),
                  ("modification54.json", "cancelation type format not valid"),
                  ("modification57.json", "Bad label reason"),
                  ("modification60.json", "the reason is not valid"),
                  ]

class TestGetVaccineDate(TestCase):
    """Class for testing get_vaccine_date"""
    @freeze_time("2022-03-08")
    def test_cancel_vacine_ok(self):
        """test ok"""
        file_test = JSON_FILES_RF3_PATH + "valid.json"
        preparation_file = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

    #first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_cancel = CancelAppointmentJsonStore()
        file_store_cancel.delete_json_file()


    # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular","+34123456789","6")
    #check the method
        my_manager.get_vaccine_date(preparation_file, "2022-08-15")
        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "4d72d2670ce85dc9b368d138ddca7daacd8bee027bc44c7c4dc5b3309286a079")
    #check store_date
        self.assertIsNotNone(file_store_cancel.find_item(value))

    @freeze_time("2022-03-08")
    def test_get_vaccine_date_no_ok_parameter(self):
        """tests no ok"""
        my_manager = VaccineManager()
        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = CancelAppointmentJsonStore()
        file_store_date.delete_json_file()
        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        file_test = JSON_FILES_RF2_PATH + 'test_ok.json'
        hash_original = file_store_date.data_hash()
        my_manager.get_vaccine_date(file_test, "2022-08-15")

        for file_name in param_list_nok:
            with self.subTest(test=file_name):
                file_test_cancelation = JSON_FILES_RF3_PATH + file_name
                # check the method
                with self.assertRaises(VaccineManagementException) as c_m:
                    my_manager.cancel_appointment(file_test_cancelation)
                self.assertEqual(c_m.exception.message, "JSON Decode Error - Wrong JSON Format")

                # read the file again to compare
                hash_new = file_store_date.data_hash()

                self.assertEqual(hash_new, hash_original)

