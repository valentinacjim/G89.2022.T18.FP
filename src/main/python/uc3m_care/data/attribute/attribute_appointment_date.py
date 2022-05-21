"""Class for the attribute AppointmentDate"""
import re
from datetime import datetime
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


# pylint: disable=too-few-public-methods
class AppointmentDate(Attribute):
    """Class for the attribute AppointmentDate"""
    _validation_pattern = r"^\d{4}([-])(0?[1-9]|1[1-2])\1(3[01]|[12][0-9]|0?[1-9])$"
    _validation_error_message = "appointment date is not valid"

    def _validate(self, attr_value: str) -> str:
        """Validates the appointment date according to the requirements"""
        registration_type_pattern = re.compile(self._validation_pattern)
        res = registration_type_pattern.fullmatch(attr_value)
        if not res:
            raise VaccineManagementException(self._validation_error_message)
        if not isinstance(datetime.fromisoformat(attr_value), datetime):
            raise VaccineManagementException(self._validation_error_message)
        today = datetime.today().date()
        if datetime.fromisoformat(attr_value).date() <= today:
            raise VaccineManagementException(self._validation_error_message)
        return attr_value
