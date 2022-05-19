"""Class for the attribute AppointmentDate"""
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from datetime import datetime

#pylint: disable=too-few-public-methods
class AppointmentDate(Attribute):
    """Class for the attribute AppointmentDate"""
    _validation_error_message = "appointment date is not valid"

    def _validate( self, attr_value: str ) -> str:
        """Validates the appointment date according to the requirements"""
        if type(datetime.fromisoformat(attr_value)) != datetime:
            raise VaccineManagementException(self._validation_error_message)
        today = datetime.today().date()
        if datetime.fromisoformat(attr_value).date() <= today:
            raise VaccineManagementException(self._validation_error_message)
        return attr_value