"""Tests for cancel_appointment method"""
from unittest import TestCase
import os
import shutil
from freezegun import freeze_time
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care import JSON_FILES_PATH, JSON_FILES_RF3_PATH
from uc3m_care import CancelAppoimentJsonStore
from uc3m_care import PatientsJsonStore


param_list_nok = ["duplication1.json","deletion1.json","duplication2.json","deletion2.json","duplication3.json",
                  "deletion3.json","duplication4.json","deletion4.json","duplication6.json","deletion6.json",
                  "duplication7.json","deletion7.json","duplication8.json","deletion8.json","duplication9.json",
                  "deletion9.json","duplication10.json","deletion10.json","duplication12.json","deletion12.json",
                  "duplication13.json","deletion13.json","duplication14.json","deletion14.json","duplication16.json",
                  "deletion16.json","duplication17.json","deletion17.json","duplication18.json","deletion18.json",
                  "duplication20.json","deletion20.json","duplication21.json","deletion21.json","duplication22.json",
                  "deletion22.json","duplication23.json","deletion23.json","duplication24.json","deletion24.json",
                  "duplication25.json","deletion25.json","duplication27.json","deletion27.json","duplication28.json",
                  "deletion28.json","duplication29.json","deletion29.json","duplication30.json","deletion30.json",
                  "duplication31.json","deletion31.json","duplication32.json","deletion32.json","duplication34.json",
                  "deletion34.json","duplication35.json","deletion35.json","duplication36.json","deletion36.json",
                  "duplication37.json","deletion37.json","duplication38.json","deletion38.json","duplication39.json",
                  "deletion39.json","duplication41.json","deletion41.json","duplication42.json","deletion42.json",
                  "duplication43.json","deletion43.json","modification5.json","modification11.json",
                  "modification15.json","modification19.json","modification26.json","modification33.json",
                  "modification40.json","modification44.json","modification45.json","modification46.json",
                  "modification47.json","modification48.json","modification49.json","modification50.json",
                  "modification51.json","modification52.json","modification53.json","modification54.json",
                  "modification55.json","modification56.json","modification57.json","modification58.json",
                  "modification59.json","modification60.json","modification61.json"]

class TestGetVaccineDate(TestCase):
    """Class for testing get_vaccine_date"""
    @freeze_time("2022-03-08")
    def test_cancel_vacine_ok(self):
        """test ok"""
        file_test = JSON_FILES_RF3_PATH + "valid.json"
        my_manager = VaccineManager()

    #first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_cancel = CancelAppoimentJsonStore()
        file_store_cancel.delete_json_file()

    # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular","+34123456789","6")
    #check the method
        my_manager.get_vaccine_date(file_test, "2022-08-15")
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
        file_store_date = CancelAppoimentJsonStore()
        file_store_date.delete_json_file()
        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        for file_name in param_list_nok:
            with self.subTest(test=file_name):
                file_test = JSON_FILES_RF3_PATH + file_name
                hash_original = file_store_date.data_hash()
                my_manager.get_vaccine_date(file_test, "2022-08-15")
                # check the method
                with self.assertRaises(VaccineManagementException) as c_m:
                    my_manager.cancel_appointment(file_test)
                self.assertEqual(c_m.exception.message, "Invalid Json structure")

                # read the file again to compare
                hash_new = file_store_date.data_hash()

                self.assertEqual(hash_new, hash_original)


    @freeze_time("2022-03-08")
    def test_get_vaccine_date_no_ok(self):
        """# long 32 in patient system id , not valid"""
        file_test = JSON_FILES_RF2_PATH + "test_no_ok.json"
        my_manager = VaccineManager()
        file_store_date = AppointmentsJsonStore()

        # read the file to compare file content before and after method call
        hash_original = file_store_date.data_hash()

        #check the method
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.get_vaccine_date(file_test, "2022-08-15")
        self.assertEqual(c_m.exception.message, "patient system id is not valid")

        # read the file again to campare
        hash_new = file_store_date.data_hash()

        self.assertEqual(hash_new, hash_original)

    @freeze_time("2022-03-08")
    def test_get_vaccine_date_no_ok_no_quotes(self):
        """ no quotes , not valid """
        file_test = JSON_FILES_RF2_PATH + "test_nok_no_comillas.json"
        my_manager = VaccineManager()
        file_store_date = AppointmentsJsonStore()

        # read the file to compare file content before and after method call
        hash_original = file_store_date.data_hash()

    #check the method
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.get_vaccine_date(file_test, "2022-08-15")
        self.assertEqual(c_m.exception.message, "JSON Decode Error - Wrong JSON Format")

    #read the file again to campare
        hash_new = file_store_date.data_hash()

        self.assertEqual(hash_new, hash_original)


    @freeze_time("2022-03-08")
    def test_get_vaccine_date_no_ok_data_manipulated( self ):
        """ no quotes , not valid """
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()
        file_store = JSON_FILES_PATH + "store_patient.json"
        file_store_date = JSON_FILES_PATH + "store_date.json"

        if os.path.isfile(JSON_FILES_PATH + "swap.json"):
            os.remove(JSON_FILES_PATH + "swap.json")
        if not os.path.isfile(JSON_FILES_PATH + "store_patient_manipulated.json"):
            shutil.copy(JSON_FILES_RF2_PATH + "store_patient_manipulated.json",
                        JSON_FILES_PATH + "store_patient_manipulated.json")

        #rename the manipulated patient's store
        if os.path.isfile(file_store):
            print(file_store)
            print(JSON_FILES_PATH + "swap.json")
            os.rename(file_store, JSON_FILES_PATH + "swap.json")
        os.rename(JSON_FILES_PATH + "store_patient_manipulated.json",file_store)

        file_store_date = AppointmentsJsonStore()
        # read the file to compare file content before and after method call
        hash_original = file_store_date.data_hash()

        # check the method

        exception_message = "Exception not raised"
        try:
            my_manager.get_vaccine_date(file_test, "2022-08-15")
        #pylint: disable=broad-except
        except Exception as exception_raised:
            exception_message = exception_raised.__str__()

        #restore the original patient's store
        os.rename(file_store, JSON_FILES_PATH + "store_patient_manipulated.json")
        if os.path.isfile(JSON_FILES_PATH + "swap.json"):
            print(JSON_FILES_PATH + "swap.json")
            print(file_store)
            os.rename(JSON_FILES_PATH + "swap.json", file_store)

        # read the file again to campare
        hash_new = file_store_date.data_hash()

        self.assertEqual(exception_message, "Patient's data have been manipulated")
        self.assertEqual(hash_new, hash_original)
