"""Subclass of JsonStore for managing the cancelation of appointments"""

from uc3m_care.storage.json_store import JsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class CancelAppointmentJsonStore():
    """Implements the singleton pattern"""
    # pylint: disable=invalid-name
    class __CancelAppointmentJsonStore(JsonStore):
        """Subclass of JsonStore for managing the Appointments"""
        _FILE_PATH = JSON_FILES_PATH + "store_cancel.json"
        _ID_FIELD = "_VaccinationAppointmentCancellation__date_signature"
        ERROR_INVALID_APPOINTMENT_OBJECT = "Invalid appointment object"

        def add_item(self, item):
            """Overrides the add_item method to verify the item to be stored"""
            # pylint: disable=import-outside-toplevel, cyclic-import
            from uc3m_care.data.vaccination_appointment_cancel \
                import VaccinationAppointmentCancellation
            if not isinstance(item, VaccinationAppointmentCancellation):
                raise VaccineManagementException(self.ERROR_INVALID_APPOINTMENT_OBJECT)
            super().add_item(item)

    instance = None

    def __new__ ( cls ):
        if not CancelAppointmentJsonStore.instance:
            CancelAppointmentJsonStore.instance = \
                CancelAppointmentJsonStore.__CancelAppointmentJsonStore()
        return CancelAppointmentJsonStore.instance

    def __getattr__ ( self, nombre ):
        return getattr(self.instance, nombre)

    def __setattr__ ( self, nombre, valor ):
        return setattr(self.instance, nombre, valor)
