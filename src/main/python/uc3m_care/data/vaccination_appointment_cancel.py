"""Contains the class Vaccination Appointment Cancellation"""
from datetime import datetime
from uc3m_care.storage.cancel_appointment_json_store import CancelAppointmentJsonStore
from uc3m_care.parser.appointment_cancellation_json_parser import AppointmentCancellationJsonParser
from uc3m_care.data.attribute.attribute_date_signature import DateSignature
from uc3m_care.data.attribute.attribute_cancelation_type import CancelationType
from uc3m_care.data.attribute.attribute_reason import Reason
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage.appointments_json_store import AppointmentsJsonStore
from uc3m_care.storage.vaccination_json_store import VaccinationJsonStore
class VaccinationAppointmentCancellation():
    """Contains the class Vaccination Appointment Cancellation"""
    def __init__(self, date_signature, cancellation_type, reason):
        self.__date_signature = DateSignature(date_signature).value
        self.__cancellation_type = CancelationType(cancellation_type).value
        self.__reason = Reason(reason).value

    @property
    def date_signature(self):
        """Property that represents the date signature"""
        return self.__date_signature

    @date_signature.setter
    def date_signature(self, value):
        self.__date_signature = value

    @property
    def cancellation_type(self):
        """Property that represents the cancellation cancellation_type"""
        return self.__cancellation_type

    @cancellation_type.setter
    def cancellation_type(self, value):
        self.__cancellation_type = value

    @property
    def reason(self):
        """Property that represents the reason to cancel"""
        return self.__reason

    @reason.setter
    def reason(self, value):
        self.__reason = value

    def save_cancel(self):
        """Function save cancel appointment"""
        cancel_store = CancelAppointmentJsonStore()
        cancel_store.add_item(self)

    @classmethod
    def get_appointment_from_date_signature(cls, date_signature):
        """returns the vaccination appointment object for the date_signature received"""
        appointments_store = CancelAppointmentJsonStore()
        appointment_record = appointments_store.find_item(DateSignature(date_signature).value)
        if appointment_record is None:
            raise VaccineManagementException("date_signature is not found")
        # freezer = freeze_time(
        #     datetime.fromtimestamp(appointment_record["_VaccinationAppointment__issued_at"]))
        # freezer.start()
        appointment = cls(appointment_record["_CancelAppointment__date_signature"],
                          appointment_record["_CancelAppointment__cancellation_type"],
                          appointment_record["_CancelAppointment__reason"])
        # freezer.stop()
        return appointment

    @classmethod
    def create_appointment_from_json_file(cls, json_file):
        """returns the vaccination appointment for the received input json file"""

        appointment_parser = AppointmentCancellationJsonParser(json_file)
        new_appointment = cls(
            appointment_parser.json_content[appointment_parser.DATE_SIGNATURE_KEY],
            appointment_parser.json_content[appointment_parser.CANCELLATION_TYPE_KEY],
            appointment_parser.json_content[appointment_parser.REASON_KEY],
        )
        appointment_store = AppointmentsJsonStore()
        appointment_data = \
            appointment_store.find_item(DateSignature(new_appointment.date_signature).value)
        if appointment_data is None:
            raise VaccineManagementException("The appointment received does not exist.")
        if datetime.fromisoformat(
                appointment_data["_VaccinationAppointment__appointment_date"]).date() < \
                datetime.today().date():
            raise VaccineManagementException("The appointment date received has already passed.")
        vaccine_store = VaccinationJsonStore()
        if vaccine_store.find_item(DateSignature(new_appointment.date_signature).value) is not None:
            raise VaccineManagementException("Vaccine has already been administered.")
        cancel_store = CancelAppointmentJsonStore()
        if cancel_store.find_item(DateSignature(new_appointment.date_signature).value) is not None:
            raise VaccineManagementException("Appointment has already been canceled.")
        return new_appointment
